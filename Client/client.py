import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.4"
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
    
def receiveFile (fileAddr):
    file = open(fileAddr, 'wb')
    file_data = client.recv(2048).decode(FORMAT)
    file.write(file_data)
    file.close()
    print("File has been received successfully.")

def receiveList(result_length): #no dg doi nhan dc cau gi do de cho vap length
    result = [[]]
    temp = []

    for i in range(result_length):
        for j in range(5):
            received_data = send("msg received")
            print(received_data + "\n")
            temp.append(received_data)
            print(temp)
        result.append(temp)
        print(result)
        temp.clear()
        print(temp)
        
    
    return result
