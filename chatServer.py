import socket
import threading
import queue

messages = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))


def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((messages, addr))
        except:
            pass


def read():
    while True:
        while not messages.empty():
            data, addr = messages.get()
            message = data.decode().strip()[1:].split(" ")
            print(message[1] + " " + message[2])
            
            if message[0] == "/join":
                if addr not in clients:
                    clients.append(addr)
            for client in clients:
                try:
                    if message.decode()[1:].startswith("/join"):
                        name = message.decode()[message.decode().index(":")+1]
                        server.sendto(f"{name} joined", client)
                    else:
                        server.sendto(message)
                except:
                    clients.remove(client)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(targer=read)

t1.start()
t2.start()
