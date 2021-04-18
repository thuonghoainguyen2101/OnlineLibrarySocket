from server_support import *
from sqlServerConn import *

 #create new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
    
#
def handle_client(conn, addr):
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        print(f"[{addr}] {msg}")

        check = False #check if Client log in or sign up succesaful to do the next task

        if msg == "LOG IN":
            check = check_log_in(conn)
            if check:
                handle_cmd(conn)
        elif msg == "SIGN UP":
            check = check_sign_up(conn)
            if check:
                handle_cmd(conn)
        elif msg == DISCONNECT_MESSAGE:
            conn.send("BYE".encode(FORMAT))

    ACTIVE_USERS.remove(conn)
    conn.close()

def send(conn, msg):
    conn.send(msg.encode(FORMAT))

def receive(conn):
    return 


#START
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        ACTIVE_USERS.append(conn)
        print(ACTIVE_USERS)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def sendFile(fileAddr):
    file = open(fileAddr, 'wb')
    file_data = s.recv(1024)
    file.write(file_data)
    file.close()
    print("File has been received successfully.")

#main
#load ACCOUNT 
load_ACCOUNT(ACCOUNT)
print(ACCOUNT)

print(f"[STARTING] server is starting...")
start()
