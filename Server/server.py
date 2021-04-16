from server_support import *

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

        if msg == "LOG IN":
            check_log_in(conn)
        elif msg == "SIGN UP":
            check_sign_up(conn)

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
        print(ACTIVE_USERS)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

#main
#load ACCOUNT 
load_ACCOUNT(ACCOUNT)
print(ACCOUNT)

print(f"[STARTING] server is starting...")
start()



