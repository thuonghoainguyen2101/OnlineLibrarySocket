import socket

HEADER = 2048
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.19"
ADDR = (SERVER, PORT)

DOWNLOAD_PATH = "D:\\1_19127287_19127568\\Source\\Client\\download"

 #create new socket and connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
#print(client.recv(2048).decode(FORMAT))

def send(msg):
    client.send(msg.encode(FORMAT))

def receive():
    res = client.recv(HEADER).decode(FORMAT)
    return res
    
def receiveFile (fileAddr):
    file = open(fileAddr, 'w', encoding=FORMAT)
    file_data = receive()
    file.write(file_data)
    file.close()
    print("File has been received successfully.")
    file.close()   

#funtion to receive search result and store it in a list of dictionaries, return the list
def receiveList():
    resultList = []
    resultRow = {}

    data = ""
    while (data != "END OF DATA"):
        data = receive()
        if data == "END OF DATA":
            break

        resultRow.update({ "ID" : data })
        data = receive()

        resultRow.update({ "NAME" : data })
        data = receive()

        resultRow.update({ "AUTHOR" : data })
        data = receive()

        resultRow.update({ "YEAR" : data })
        data = receive()

        resultRow.update({ "TYPE" : data })

        print(resultRow)
        resultList.append(resultRow.copy())
        print(resultList)
    
    print(resultList)
    return resultList
