import socket
import threading
import queue
import json

messages = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))


def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass


def read():
    while True:
        while not messages.empty():
            data, addr = messages.get()
            message = json.loads(data.decode())
            reply = {}
            print("System Recieved: " + data.decode() + "\n")
            print("Sender Info: " + addr.decode() + "\n")
        
            if message["command"] == "join":
                if addr not in clients:
                    clients.append(addr)
                reply = {'message':"connected"}
                server.sendto(reply, addr)
            else:
                reply = {'message':'received'}

t1 = threading.Thread(target=receive)
t2 = threading.Thread(targer=read)

t1.start()
t2.start()
