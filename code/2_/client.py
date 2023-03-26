import socket
import sys

import select
import errno

HEADER_LENGTH = 64

SERVER = "192.168.1.18"  # might need to change -- in cmd run: ipconfig, look for upv4 address
# SERVER = socket.gethostbyname(socket.gethostname())  # gets ip automatically
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


my_username = input("Username: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client.setblocking(False)  # receive functionality isn't blocking ?

username = my_username.encode(FORMAT)
username_header = f"{len(username):<{HEADER_LENGTH}}".encode(FORMAT)
client.send(username_header + username)

while True:
    message = input(f"{my_username} > ")

    if message:
        msg = message.encode(FORMAT)
        msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode(FORMAT)
        client.send(msg_header + msg)
    try:
        while True:
            username_header = client.recv(HEADER_LENGTH)
            if not len(username_header):  # NO DATA
                print("[C CONNECTION] by server")
                sys.exit()
            username_length = int(username_header.decode(FORMAT).strip())
            username = client.recv(username_length).decode(FORMAT)

            msg_header = client.recv(HEADER_LENGTH)
            msg_length = int(msg_header.decode(FORMAT).strip())
            msg = client.recv(msg_length).decode(FORMAT)

            print(f"{username} > {msg}")

    # e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK
    # these 2 errors mean --> nothing more to receive, which is normal

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error,', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()
