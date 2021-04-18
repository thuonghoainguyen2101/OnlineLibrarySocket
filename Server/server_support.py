import socket 
import threading

from sqlServerConn import *

#define
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

ACTIVE_USERS = []

ACCOUNT = {"admin" : "@@"}
ACCOUNT_PATH = "D:\SOCKET_PROJ\Server/account.txt"

#function to send message to all user
def sendall(msg):
    for conn in ACTIVE_USERS:
        conn.send(msg.encode(FORMAT))

#function to load data from account file to ACCOUNT
def load_ACCOUNT(ACCOUNT):
    with open(ACCOUNT_PATH, "r") as f:        
        while True:
            x = f.readline()
            x = x.replace("\n", "")
            if not x: #reach the end of file
                break
            y = f.readline()
            y = y.replace("\n", "")

            ACCOUNT.update({x : y})

    print(ACCOUNT)


#LOGIN
def check_log_in(conn):
    #nhan username va password tu client
    conn.send("YOU ARE LOGGING IN". encode(FORMAT))
    
    username_length = conn.recv(HEADER).decode(FORMAT)
    username_length = int (username_length)
    username = conn.recv(username_length).decode(FORMAT)
    print("user: " + username)
    conn.send("msg received".encode(FORMAT))
    
    password_length = conn.recv(HEADER).decode(FORMAT)
    password_length = int (password_length)
    password = conn.recv(password_length).decode(FORMAT)
    print("pass: " + password)

    #kiem tra xem co phai tin nhan dong ket noi khong
    if (username != DISCONNECT_MESSAGE and password != DISCONNECT_MESSAGE):
    #kiem tra xem co trong ACCOUNT hay khong
        if username in ACCOUNT and ACCOUNT[username] == password:
            conn.send("LOG IN SUCCEED".encode(FORMAT))
            return True
        else:
            conn.send("LOG IN FAILED".encode(FORMAT))
            return False
    else: conn.send("BYE".encode(FORMAT))

#SIGNUP
def check_sign_up(conn):
    #nhan username va password tu client
    conn.send("YOU ARE SIGNING UP". encode(FORMAT))
    
    username_length = conn.recv(HEADER).decode(FORMAT)
    username_length = int (username_length)
    username = conn.recv(username_length).decode(FORMAT)
    print("user: " + username)
    conn.send("msg received".encode(FORMAT))
    
    password_length = conn.recv(HEADER).decode(FORMAT)
    password_length = int (password_length)
    password = conn.recv(password_length).decode(FORMAT)
    print("pass: " + password)

    #kiem tra co phai tin nhan dong ket noi khong
    if (username != DISCONNECT_MESSAGE):
    #kiem tra xem co trong ACCOUNT hay khong
        if username in ACCOUNT:
            conn.send("SIGN UP FAILED".encode(FORMAT))
        else:
            ACCOUNT.update({username : password})
            #add new account into file
            with open(ACCOUNT_PATH, "a") as f: 
                f.writelines("\n" + username + "\n" + password)
        conn.send("SIGN UP SUCCEED".encode(FORMAT))
        return True
    else: 
        conn.send("BYE".encode(FORMAT))
        return False

def handle_cmd(conn):
    #receive msg from client
    cmd_length = conn.recv(HEADER).decode(FORMAT)
    cmd_length = int(cmd_length)
    cmd = conn.recv(cmd_length).decode(FORMAT)

    #execute the cmd
    cmd_split = cmd.split(' ')

    result = []

    if cmd_split[0] == "F_ID":
        result = selectByID(cmd_split[1])
    if cmd_split[0] == "F_NAME":
        result = selectByName(cmd_split[1])
    if cmd_split[0] == "F_AUTHOR":
        result = selectByAuthor(cmd_split[1])
    if cmd_split[0] == "F_TYPE":
        result = selectByType(cmd_split[1])

    #send number of result to client
    temp = result.fetchall()
    result_length = len(temp)
    print(result_length)
    conn.send((str(result_length)).encode(FORMAT))
    print(result_length)
    #send each row of the result list to client
    for row in result:
        send_row(conn, row)

#function to send 1 row of result to client
def send_row(conn, row):

    conn.send((row.ID).encode(FORMAT))
    print("send success")

    cmd_length = conn.recv(HEADER).decode(FORMAT)
    cmd_length = int(cmd_length)
    cmd = conn.recv(cmd_length).decode(FORMAT)
    conn.send((row.NAMEOFBOOK).encode(FORMAT))
    print("send success")

    cmd_length = conn.recv(HEADER).decode(FORMAT)
    cmd_length = int(cmd_length)
    cmd = conn.recv(cmd_length).decode(FORMAT)
    conn.send((row.NAMEOFAUTHOR).encode(FORMAT))
    print("send success")

    cmd_length = conn.recv(HEADER).decode(FORMAT)
    cmd_length = int(cmd_length)
    cmd = conn.recv(cmd_length).decode(FORMAT)
    conn.send(str(row.PUBLISHYEAR).encode(FORMAT))
    print("send success")

    cmd_length = conn.recv(HEADER).decode(FORMAT)
    cmd_length = int(cmd_length)
    cmd = conn.recv(cmd_length).decode(FORMAT)
    conn.send((row.TYPEOFBOOK).encode(FORMAT))
    print("send success")

