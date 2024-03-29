import socket
import threading
import random
import json
import time



client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#declare a global variable for determining if join is successful
global join
join = False
#declare a global variable for determining if register is successful
global register
register = False

run = True


# Set the timeout to 60 seconds
# this will detect if the server has stopped running after 60 seconds
client.settimeout(60)

def receive():
    while True:
        try:
            msg, _ = client.recvfrom(1024)
            message = json.loads(msg.decode())
            print(message['message'])

            # global variable for checking whether joining is successful
            if message['message'] == "Connection to the Message Board Server is successful!":
                global join
                join = True
            #global variable for checking whether register is successful
            elif message['message'] != "Error: Registration failed. Handle or alias already exists.":
                global register
                register = True
        except socket.timeout:
        # If no data is received within the timeout, raise an error
            raise RuntimeError("Connection to server lost. No data received within the timeout period.")   
        except:
            pass



print('START INPUT:')
while run is True:
    enter = input("")
    command = enter.split()[0]

    #first command should be join to connect to the server
    if command == "/join":
        try:
            host = enter.split()[1]
            port = int(enter.split()[2])
            client.bind((host, random.randint(8000, 9000)))
            t = threading.Thread(target=receive)
            t.start()
            payload = {"command": "join"}
            client.sendto(str.encode(json.dumps(payload)), (host, port))
            time.sleep(0.5)

            while join is True:
                enter = input("")
                command = enter.split()[0]

                #user should register after joining
                if command == "/register":
                    try:
                        name = enter.split()[1]
                        print(name)
                        payload = {"command": "register"}
                        payload["handle"] = name
                        client.sendto(str.encode(json.dumps(payload)), (host, port))
                        time.sleep(0.5)

                        while register is True:
                            enter = input("")
                            command = enter.split()[0]

                            if command == "/leave":
                                payload = {"command": "leave"}
                                client.sendto(str.encode(json.dumps(payload)), (host, port))
                                time.sleep(0.5)
                                join = False
                                register = False
                                run = False
                            elif command == "/?":
                                print("/join to connect to a chatroom")
                                print("/leave to disconnect from a chatroom")
                                print("/register to register a handle")
                                print("/all to send a message to all users")
                                print("/msg to send a message to a specific user")
                                print("/? to show help menu")
                            elif command == "/all":
                                recipient = "all"
                                try:
                                    message = enter.split(" ", 1)[1]
                                    payload = {"command": "all"}
                                    payload["message"] = message
                                    client.sendto(str.encode(json.dumps(payload)), (host, port))
                                    time.sleep(0.5)
                                except:
                                    print('Error: Unsuccesful sending of message.')
                            elif command == "/msg":
                                try:
                                    recipient = enter.split()[1]
                                    message = enter.split(" ", 2)[2]
                                    payload = {"command": "msg"}
                                    payload["handle"] = recipient
                                    payload["message"] = message
                                    client.sendto(str.encode(json.dumps(payload)), (host, port))
                                    time.sleep(0.5)
                                except:
                                    print('Error: Unsuccesful sending of message.')
                            else:
                                payload = {"command": "random"}
                                client.sendto(str.encode(json.dumps(payload)), (host, port))
                                time.sleep(0.5)
                    except:
                        print('Error: Unsuccessful register.')
                elif command == "/leave":
                    payload = {"command": "leave"}
                    client.sendto(str.encode(json.dumps(payload)), (host, port))
                    time.sleep(0.5)
                    join = False
                    run = False
                elif command == "/?":
                            print("/join to connect to a chatroom")
                            print("/leave to disconnect from a chatroom")
                            print("/register to register a handle")
                            print("/all to send a message to all users")
                            print("/msg to send a message to a specific user")
                            print("/? to show help menu")
                else:
                    payload = {"command": "random"}
                    client.sendto(str.encode(json.dumps(payload)), (host, port))
                    time.sleep(0.5)

        except:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")

    elif command == "/leave":
        print("Error: Disconnection failed. Please connect to the server first.")
    elif command == "/?":
        #show help menu
        print("--- here are the following commands ---")
        print("/join to connect to a chatroom")
        print("/leave to disconnect from a chatroom")
        print("/register to register a handle")
        print("/all to send a message to all users")
        print("/msg to send a message to a specific user")
        print("/? to show help menu")
    else:
        print("Error: Command not found.")

