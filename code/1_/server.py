import socket
import threading

### https://youtu.be/3QiPPX-KeSc?t=2428
### https://www.youtube.com/watch?v=3QiPPX-KeSc @ 40:28

HEADER = 64
PORT = 5050
# SERVER = "192.168.1.18"  # might need to change -- in cmd run: ipconfig, look for upv4 address
SERVER = socket.gethostbyname(socket.gethostname())  # gets ip automatically
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # family and type are the arguments
# socket.AF_INET --> allowing connections of type ipv4
# socket.SOCK_STREAM --> sending data through the socket
server.bind(ADDR)  # bind the created server (socket) to the address


# basically we are saying that whoever connects to that address, will see the socket


# handles a connection to a single client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # each message is two-fold
        # first is a message saying how many bytes the real message will be
        # second message is the actual message itself
        msg_len = conn.recv(HEADER).decode(FORMAT)  # how many bytes we accept
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")

    conn.close()


# handles new connections
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # we are waiting for a new connection, this line blocks the thread
        conn, addr = server.accept()  # when a new connection occurs we advance in the while
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[#CONNECTIONS] {threading.active_count() - 1}")
        # -1 --> because 1 of the threads is the server itself


print("[STARTING ] Server is starting ...")
start()
