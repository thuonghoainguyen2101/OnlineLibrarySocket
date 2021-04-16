import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.9"
ADDR = (SERVER, PORT)

 #create new socket and connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
#print(client.recv(2048).decode(FORMAT))

#function to send msg to server, return the message from server back to client
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    return client.recv(2048).decode(FORMAT)
    
# main
#send(DISCONNECT_MESSAGE)