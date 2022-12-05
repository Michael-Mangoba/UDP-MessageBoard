import socket
import threading
import queue
import json

messages = queue.Queue()
clients = []
handles = []
Buffer = 1024
UDP_Host_IP = "localhost"
UDP_Host_Port = 7890

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
            content = ""
            host, port = addr
            print("System Recieved: " + data.decode() + "\n")
            print("Sender Info: " + host + " " + str(port) + "\n")
        
            if message["command"] == "join":
                if addr not in clients:
                    clients.append(addr)
                    handles.append("")
                content = "Connection to the Message BoardServer is successful!"
                reply = {'message': content}
                server.sendto(str.encode(json.dumps(reply)), addr)
            elif message["command"] == "leave":
                clients.remove(addr)
                content = "Connection closed. Thank you!"
                reply = {'message': content}
                server.sendto(str.encode(json.dumps(reply)), addr)
            elif message["command"] == "register":
                if message["handle"] not in handles:
                    index = clients.index(addr)
                    handles[index] = message["handle"]
                    newHandle = message["handle"]
                    content = "Welcome {}".format(newHandle)
                    reply = {'message': content}
                    server.sendto(str.encode(json.dumps(reply)), addr)
                else:
                    content = "Error: Registration failed. Handle or alias already exists."
                    reply = {'message': content}
                    server.sendto(str.encode(json.dumps(reply)), addr)
            else:
                reply = {'message':'received'}
                server.sendto(str.encode(json.dumps(reply)), addr)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=read)

t1.start()
t2.start()
