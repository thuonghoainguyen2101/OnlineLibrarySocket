from server_support import *
from sqlServerConn import *

 #create new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
    
#
def handle_client(conn, addr):
    while True:
        msg = receive(conn)
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
            send(conn, "BYE")
            ACTIVE_USERS.remove(conn)
            conn.close()

    ACTIVE_USERS.remove(conn)
    conn.close()

#START
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        ACTIVE_USERS.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

#main
#load ACCOUNT 
load_ACCOUNT(ACCOUNT)

print(f"[STARTING] server is starting...")
start()
