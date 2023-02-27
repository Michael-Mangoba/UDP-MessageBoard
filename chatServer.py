import socket
import threading
import queue
import json

messages = queue.Queue()
clients = []
handles = []
Buffer = 1024
UDP_Host_IP = "localhost"
UDP_Host_Port = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((UDP_Host_IP, UDP_Host_Port))
print(socket.gethostbyname(UDP_Host_IP))

def receive():
    while True:
        try:
            message, addr = server.recvfrom(Buffer)
            messages.put((message, addr))
        except:
            pass


def read():
    while True:
        while not messages.empty():
            data, addr = messages.get()
            message = json.loads(data.decode())
            reply = {}
            notif = {}
            error = {}
            content = ""
            host, port = addr
            print("System Recieved: " + data.decode() + "\n")
            print("Sender Info: " + host + " " + str(port) + "\n")
            try:
#Join
                if message["command"] == "join":
                    if addr not in clients:
                        clients.append(addr)
                        handles.append("")
                    content = "Connection to the Message Board Server is successful!"
                    reply = {'command': 'join', 'message': content}
                    server.sendto(str.encode(json.dumps(reply)), addr)
#Leave
                elif message["command"] == "leave":
                    index = clients.index(addr)
                    handles.pop(index)
                    clients.remove(addr)
                    content = "Connection closed. Thank you!"
                    reply = {'command': 'leave', 'message': content}
                    server.sendto(str.encode(json.dumps(reply)), addr)
#Register
                elif message["command"] == "register":
                    if message["handle"] not in handles:
                        index = clients.index(addr)
                        handles[index] = message["handle"]
                        newHandle = message["handle"]
                        content = "Welcome {}!".format(newHandle)
                        reply = {'command': 'register', 'message': content}
                        server.sendto(str.encode(json.dumps(reply)), addr)
    #Existing Alias Error
                    else:
                        content = "Error: Registration failed. Handle or alias already exists."
                        error = {'command': 'error', 'message': content}
                        server.sendto(str.encode(json.dumps(error)), addr)
#Message All
                elif message["command"] == "all":
                    index = clients.index(addr)
                    content = "{}: {}".format(handles[index], message["message"])
                    reply = {'command': 'all', 'message': content}
                    for client in clients:
                        server.sendto(str.encode(json.dumps(reply)), client)
#Direct Message
                elif message["command"] == "msg":
                    try:
                        SenderIndex = clients.index(addr)
                        ReceiverIndex = handles.index(message["handle"])

                        content = "[From {}]: {}".format(handles[SenderIndex], message["message"])
                        reply = {'command': 'msg', 'message': content}
                        server.sendto(str.encode(json.dumps(reply)), clients[ReceiverIndex])

                        notifContent = "[To {}]: {}".format(handles[ReceiverIndex], message["message"])
                        notif = {'command': 'msg', 'message': notifContent}
                        server.sendto(str.encode(json.dumps(notif)), addr)   
    #Invalid Handle Error          
                    except:
                        content = "Error: Handle or alias not found."
                        error = {'command': 'error', 'message': content}
                        server.sendto(str.encode(json.dumps(error)), addr)
    #Invalid Command Error
                else:
                    error = {'command': 'error', 'message':'Error: Command not found.'}
                    server.sendto(str.encode(json.dumps(error)), addr)
    #Invalid Parameters Error
            except:
                error = {'command': 'error', 'message':'Error: Command parameters do not match or is not allowed.'}

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=read)

t1.start()
t2.start()
