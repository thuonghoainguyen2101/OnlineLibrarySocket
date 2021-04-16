import socket 
import threading

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
    conn.send(" ".encode(FORMAT))
    
    password_length = conn.recv(HEADER).decode(FORMAT)
    password_length = int (password_length)
    password = conn.recv(password_length).decode(FORMAT)
    print("pass: " + password)

    #kiem tra xem co phai tin nhan dong ket noi khong
    if (username != DISCONNECT_MESSAGE and password != DISCONNECT_MESSAGE):
    #kiem tra xem co trong ACCOUNT hay khong
        if username in ACCOUNT and ACCOUNT[username] == password:
            conn.send("LOG IN SUCCEED".encode(FORMAT))
        else:
            conn.send("LOG IN FAILED".encode(FORMAT))
    else: conn.send("BYE".encode(FORMAT))

#SIGNUP
def check_sign_up(conn):
    #nhan username va password tu client
    conn.send("YOU ARE SIGNING UP". encode(FORMAT))
    
    username_length = conn.recv(HEADER).decode(FORMAT)
    username_length = int (username_length)
    username = conn.recv(username_length).decode(FORMAT)
    print("user: " + username)
    conn.send(" ".encode(FORMAT))
    
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
        print (ACCOUNT)
    else: conn.send("BYE".encode(FORMAT))
