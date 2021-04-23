from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter

from server import *

load_ACCOUNT(ACCOUNT)

 #create new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    while True:
        msg = receive(conn)
        print(f"[{addr}] {msg}")

        check = False #check if Client log in or sign up successful to do the next task

        if msg == "LOG IN":
            check = check_log_in(conn)
            if check:
                cmd = receive(conn)
                handle_cmd(conn, cmd)
        elif msg == "SIGN UP":
            check = check_sign_up(conn)
            if check:
                cmd = receive(conn)
                handle_cmd(conn, cmd)
        elif msg == DISCONNECT_MESSAGE:
            send(conn, "BYE")
            ACTIVE_USERS.remove(conn)
            conn.close()

    ACTIVE_USERS.remove(conn)
    conn.close()

def center(toplevel):
    toplevel.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

def handleClosing(window):
     if messagebox.askokcancel("Quit", "Send disconnect message to all clients?"):
        sendall(DISCONNECT_MESSAGE)
        window.destroy()
        exit()    

def handleListenButton(window, n):
    notiWindow(n)

def serverWindow():
    window = Tk()
    window.title("Server's window")
    window.geometry("1000x600")
    center(window)

    nLabel = tkinter.Label(window, text="Enter max number of clients can access: ")
    nTextBox = Entry(window, width=20)
    listenButton = Button(window, text = "Start listening", command = lambda: handleListenButton(window, int(nTextBox.get())))

    nLabel.pack()
    nTextBox.pack()
    listenButton.pack()

    window.protocol("WM_DELETE_WINDOW", lambda: handleClosing(window))
    window.mainloop()

def notiWindow(n):
    window = Tk()
    window.title("Notification")
    window.geometry("1000x600")
    center(window)

    noti = Text(window, height = 10, width = 150)
    noti.pack(fill = BOTH)

    i = 0
    print (SERVER)
    server.bind((SERVER, PORT))

    noti.insert(END, f"[LISTENING] Server is listening on {SERVER}\n". format(SERVER = SERVER))
    server.listen()
    while i < n:
        i += 1
        conn, addr = server.accept()
        noti.insert(END, f"[NEW CONNECTION] {addr} connected.\n")
        ACTIVE_USERS.append(conn)
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        noti.insert(END, f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")

    window.protocol("WM_DELETE_WINDOW", lambda: handleClosing(window))
    window.mainloop()
    

#main
thread = threading.Thread(target = serverWindow)
thread.start()
