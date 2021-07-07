import socket 
import threading
import time

#define
HEADER = 2048
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HOST = socket.gethostname()

ACTIVE_USERS = []

ACCOUNT = {"admin" : "@@"}
ACCOUNT_PATH = "D:\\1_19127287_19127568\\Sourrce\\Server\\account.txt"

from sqlServerConn import *

def send(conn, msg):
    conn.send(msg.encode(FORMAT))

def receive(conn):
    res = conn.recv(HEADER).decode(FORMAT)
    return res

def sendFile(conn, fileAddr):
    file = open(fileAddr, 'r', encoding=FORMAT)
    file_data = file.read()
    send(conn, file_data)
    print ("file send success")
    file.close()

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
    password = receive(conn)
    print("pass: " + password)

    #kiem tra co phai tin nhan dong ket noi khong
    if (username != DISCONNECT_MESSAGE and password != DISCONNECT_MESSAGE):
    #kiem tra xem co trong ACCOUNT hay khong
        if username in ACCOUNT:
            send(conn, "SIGN UP FAILED")
            return False
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

def handle_cmd(conn, cmd):
    #receive msg from client
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

    fileAddr = []

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

        fileAddr.append(row.LINK)
    
    time.sleep(0.05)
    send(conn, "END OF DATA")

    continue_handle_cmd(conn, fileAddr)

def continue_handle_cmd(conn, fileAddr):
    cmd = ""
    while cmd != DISCONNECT_MESSAGE:
        cmd = receive(conn)
        print(cmd)

        if cmd[0] == 'F' and cmd[1] == '_':
            handle_cmd(conn, cmd)

        elif cmd == "VIEW":
            for addr in fileAddr:
                print(addr)            
                sendFile(conn, addr)
                time.sleep (0.2)
                print("send success")

        elif cmd == "DOWNLOAD":
            for addr in fileAddr:
                nameFile = ""
                for j in range(len(addr) - 1, 0, -1):
                    if addr[j] == '\\': break
                    nameFile = addr[j] + nameFile
                send(conn, nameFile)
                print("one punch : " + nameFile)
                sendFile(conn, addr)
                print("send success")
