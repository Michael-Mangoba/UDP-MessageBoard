import socket
import threading
import queue
import json

messages = queue.Queue()
clients = []
Buffer = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))


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
            print("System Recieved: " + data.decode() + "\n")
            print("Sender Info: " + addr.decode() + "\n")
        
            if message["command"] == "join":
                if addr not in clients:
                    clients.append(addr)
                content = "Connection to the Message BoardServer is successful!"
                reply = {'message': content}
                server.sendto(reply, addr)
            elif ["command"] == "leave":
                clients.remove(addr)
                content = "Connection closed. Thank you!"
                reply = {'message': content}
                server.sendto(reply, addr)
            else:
                reply = {'message':'received'}

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=read)

t1.start()
t2.start()
