import socket

HEADER = 2048
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.4"
ADDR = (SERVER, PORT)

 #create new socket and connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
#print(client.recv(2048).decode(FORMAT))

def send(msg):
    client.send(msg.encode(FORMAT))

def receive():
    res = client.recv(HEADER).decode(FORMAT)
    return res

#funtion to receive search result and store it in a list of dictionaries, return the list
def receiveList():
    resultList = []
    resultRow = {}

    data = ""
    while (data != "END OF DATA"):
        data = receive()
        print(data)
        print(' ')
        if data == "END OF DATA":
            break
        resultRow.update({ "ID" : data })
        data = receive()

        print(data)
        print('\n')
        resultRow.update({ "NAME" : data })
        data = receive()

        print(data)
        print('\n')
        resultRow.update({ "AUTHOR" : data })
        data = receive()

        print(data)
        print('\n')
        resultRow.update({ "YEAR" : data })
        data = receive()

        print(data)
        print('\n')
        resultRow.update({ "TYPE" : data })

        print(resultRow)
        resultList.append(resultRow)
        print(resultList)
    
    print(resultList)
    return resultList
