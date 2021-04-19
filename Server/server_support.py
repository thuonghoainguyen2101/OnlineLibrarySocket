import socket 
import threading
import time

from sqlServerConn import *

#define
HEADER = 2048
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

ACTIVE_USERS = []

ACCOUNT = {"admin" : "@@"}
ACCOUNT_PATH = "D:\SOCKET_PROJ\Server/account.txt"

def send(conn, msg):
    conn.send(msg.encode(FORMAT))

def receive(conn):
    res = conn.recv(HEADER).decode(FORMAT)
    return res

#function to send message to all user
def sendall(msg):
    for conn in ACTIVE_USERS:
        send(conn, msg)

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
    send(conn, "YOU ARE LOGGING IN")
    
    username = receive(conn)
    print("user: " + username)
    
    password = receive(conn)
    print("pass: " + password)

    #kiem tra xem co phai tin nhan dong ket noi khong
    if (username != DISCONNECT_MESSAGE and password != DISCONNECT_MESSAGE):
    #kiem tra xem co trong ACCOUNT hay khong
        if username in ACCOUNT and ACCOUNT[username] == password:
            
            send(conn, "LOG IN SUCCEED")
            return True
        else:
            send(conn, "LOG IN FAILED")
            return False
    else: 
        send(conn, "BYE")
        return False

#SIGNUP
def check_sign_up(conn):
    #nhan username va password tu client
    send(conn, "YOU ARE SIGNING UP")
    
    username = receive(conn)
    print("user: " + username)
    send(conn, "username received, give me password")
    
    password = receive(conn)
    print("pass: " + password)

    #kiem tra co phai tin nhan dong ket noi khong
    if (username != DISCONNECT_MESSAGE and password != DISCONNECT_MESSAGE):
    #kiem tra xem co trong ACCOUNT hay khong
        if username in ACCOUNT:
            send(conn, "SIGN UP FAILED")
        else:
            ACCOUNT.update({username : password})
            #add new account into file
            with open(ACCOUNT_PATH, "a") as f: 
                f.writelines("\n" + username + "\n" + password)
        send(conn, "SIGN UP SUCCEED")
        return True
    else: 
        send(conn, "BYE")
        return False

def handle_cmd(conn):
    #receive msg from client
    cmd = receive(conn)
    if cmd == DISCONNECT_MESSAGE:
        return
    print("cmd: " + cmd)
    #execute the cmd
    cmd_split = cmd.split(' ')

    if cmd_split[0] == "F_ID":
        result = selectByID(cmd_split[1])
    if cmd_split[0] == "F_NAME":
        result = selectByName(cmd_split[1])
    if cmd_split[0] == "F_AUTHOR":
        result = selectByAuthor(cmd_split[1])
    if cmd_split[0] == "F_TYPE":
        result = selectByType(cmd_split[1])

    #send each row of the result list to client
    for row in result:
        print (row)
        send(conn, row.ID)
        time.sleep(0.05)
        send(conn, row.NAMEOFBOOK)
        time.sleep(0.05)
        send(conn, row.NAMEOFAUTHOR)
        time.sleep(0.05)
        send(conn, str(row.PUBLISHYEAR))
        time.sleep(0.05)
        send(conn, row.TYPEOFBOOK)
    
    time.sleep(0.05)
    send(conn, "END OF DATA")
    print("send success")
