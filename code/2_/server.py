import socket
import select

HEADER_LENGTH = 64

# SERVER = "192.168.1.18"  # might need to change -- in cmd run: ipconfig, look for upv4 address
SERVER = socket.gethostbyname(socket.gethostname())  # gets ip automatically
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # family and type are the arguments
# socket.AF_INET --> allowing connections of type ipv4
# socket.SOCK_STREAM --> sending data through the socket

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # IDK
server.bind(ADDR)  # bind the created server (socket) to the address

sockets_list = [server]  # list of clients

clients = {}


def receive_message(client_socket):
    try:
        msg_header = client_socket.recv(HEADER_LENGTH)
        if not len(msg_header):
            return False
        msg_len = int(msg_header.decode(FORMAT).strip())
        return {
            "header": msg_header,
            "data": client_socket.recv(msg_len)
        }
    except:
        return False


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in read_sockets:
            if notified_socket == server:
                # someone just connected
                client_socket, client_address = server.accept()
                user = receive_message(client_socket)
                if user is False:
                    continue
                sockets_list.append(client_socket)
                clients[client_socket] = user
                username = user['data'].decode(FORMAT)
                print(f"[N CONNECTION] from {client_address[0]}:{client_address[1]} -- user:{username}")
            else:
                # already known user
                msg = receive_message(notified_socket)
                user = clients[notified_socket]
                username = user['data'].decode(FORMAT)
                if msg is False:
                    print(f"[C CONNECTION] with {username}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                print(f"[N MESSAGE] from {username}: {msg['data'].decode(FORMAT)}")

                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(user['header'] + user['data'] + msg['header'] + msg['data'])

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]


print("[STARTING ] Server is starting ...")

start()
