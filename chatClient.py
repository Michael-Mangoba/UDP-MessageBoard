import socket
import threading
import random
import json
import time

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def receive():
    while True:
        try:
            msg, _ = client.recvfrom(1024)
            message = json.loads(msg.decode())
            print(message['message'])
        except:
            pass


while True:
    enter = input("Command: ")
    command = enter.split()[0]

    if command == "/join":
        host = enter.split()[1]
        port = int(enter.split()[2])
        client.bind((host, random.randint(8000, 9000)))
        t = threading.Thread(target=receive)
        t.start()
        payload = {"command": "join"}
        client.sendto(str.encode(json.dumps(payload)), (host, port))
        time.sleep(0.5)

        while True:
            enter = input("Command: ")
            command = enter.split()[0]

            if command == "/register":
                name = enter.split()[1]
                payload = {"command": "register"}
                payload["handle"] = name
                client.sendto(str.encode(json.dumps(payload)), (host, port))
                time.sleep(0.5)

                while True:
                    enter = input("Command: ")
                    command = enter.split()[0]

                    if command == "/leave":
                        payload = {"command": "leave"}
                        client.sendto(str.encode(json.dumps(payload)), (host, port))
                        exit()
                    elif command == "/?":
                        print("lol")
                    elif command == "/all":
                        recipient = "all"
                        message = enter.split(" ", 1)[1]
                        payload = {"command": "all"}
                        payload["message"] = message
                        client.sendto(str.encode(json.dumps(payload)), (host, port))
                        time.sleep(0.5)
                    elif command == "/msg":
                        recipient = enter.split()[1]
                        message = enter.split(" ", 2)[2]
                        payload = {"command": "msg"}
                        payload["handle"] = recipient
                        payload["message"] = message
                        client.sendto(str.encode(json.dumps(payload)), (host, port))
                        time.sleep(0.5)

            elif command == "/leave":
                payload = {"command": "leave"}
                client.sendto(str.encode(json.dumps(payload)), (host, port))
                exit()
            elif command == "/?":
                print("lol")
            else:
                print("register first")

    elif command == "/leave":
        exit()
    elif command == "/?":
        print("lol")
    else:
        print(enter, "join first")
