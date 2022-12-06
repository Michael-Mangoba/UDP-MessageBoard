import socket
import threading
import random
import json
import time
import select

# To do:
# - add timeout in client side
# - fix loop when join unsuccessful
# - fix loop when register unsuccessful
# - try catch when error
# - /? print syntax commands

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#declare a global variable for determining if join is successful
join = False
#declare a global variable for determining if register is successful
register = False

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
                    else:
                        payload = {"command": "random"}
                        client.sendto(str.encode(json.dumps(payload)), (host, port))
                        time.sleep(0.5)

            elif command == "/leave":
                payload = {"command": "leave"}
                client.sendto(str.encode(json.dumps(payload)), (host, port))
                exit()
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

# # Create a UDP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Set a timeout of 5 seconds
# timeout = 5

# # Bind the socket to a local address and port
# sock.bind(('localhost', 10000))

# # Enter the chat room loop
# while True:
#     # Wait for data on the socket with the specified timeout
#     ready = select.select([sock], [], [], timeout)

#     # Check if there is data available on the socket
#     if ready[0]:
#         # Receive data from the socket
#         data, addr = sock.recvfrom(1024)

#         # Print the received data
#         print(f'Received: {data} from {addr}')

#     # Check if the timeout has expired
#     else:
#         # Print a message indicating that no data was received
#         print('No data received')

#         # Leave the chat room
#         break
#  the timeout variable specifies the timeout in seconds. 
# The select.select() function is used to wait for data on the socket with the specified timeout.
#  If data is received on the socket within the specified timeout, 
#  it is printed to the screen. 
#  If the timeout expires without any data being received, 
#  a message is printed to the screen indicating that no data was received, 
#  and the chat room loop is terminated.
# # Close the socket