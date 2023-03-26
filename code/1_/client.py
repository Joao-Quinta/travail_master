import socket

HEADER = 64
PORT = 5050
SERVER = "192.168.1.18"  # might need to change -- in cmd run: ipconfig, look for upv4 address
# in client side you are connecting to the ip of the server
# SERVER = socket.gethostbyname(socket.hostname())  # gets ip automatically
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)  # encodes string into bytes
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)  # respects the protocol -- sends length of message
    client.send(message)  # sends message itself


send("SALUT")
send("SALUT1")
send("SALUT2")
send(DISCONNECT_MESSAGE)
