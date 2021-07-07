from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter
import tkinter.scrolledtext as st

from client import *

def center(toplevel):
    toplevel.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2


def handleClosing(window):
     if messagebox.askokcancel("Quit", "Do you want to disconnect?"):
        send(DISCONNECT_MESSAGE)
        window.destroy()
        exit()

def handleLogInButton(window):
    send("LOG IN")
    window.destroy() #hide ChoiceWindow
    inputAccountWindow()

def handleSignUpButton(window):
    send("SIGN UP")
    window.destroy() #unhide choiceWindow
    inputAccountWindow()

def choiceWindow():
    window = Tk()
    window.title("Client's choice")
    window.geometry("1000x600")
    center(window)

    logInButton = Button(window, text = "Click here to log in", command = lambda: handleLogInButton(window))
    signUpButton = Button(window, text = "Click here to sign up", command = lambda: handleSignUpButton(window))

    logInButton.pack(fill = 'x')    
    signUpButton.pack(fill = 'x')

    #send !DISCONNECT message if client hit the exit button
    window.protocol("WM_DELETE_WINDOW", lambda: handleClosing(window))
    window.mainloop()

def handleAccountClosing(window):
     if messagebox.askokcancel("Quit", "Do you want to disconnect?"):
        send(DISCONNECT_MESSAGE)
        send(DISCONNECT_MESSAGE)
        window.destroy()
        exit()

def handleSendButton(window, username, password):
    send(username)
    #print(receive())
    send(password)
    #print(receive())
    result = receive()
    print(result)

    if result == "LOG IN SUCCEED":
        messagebox.showinfo("Notification", "Log in Successful")
        window.destroy()
        searchWindow()
        
    elif result == "LOG IN FAILED":
        messagebox.showinfo("Notification", "Username or Password is incorrect, try again")
        window.destroy()
        choiceWindow()

    elif result == "SIGN UP SUCCEED":
        messagebox.showinfo("Notification", "Sign up Successful")
        window.destroy()
        searchWindow()

    elif result == "SIGN UP FAILED":
        messagebox.showinfo("Notification", "Username is used, try again")
        window.destroy()
        choiceWindow()

def inputAccountWindow():
        window = Tk()
        window.title("Client's input")
        window.geometry("1000x600")
        center(window)

        print(receive())

        usernameLabel = tkinter.Label(window, text="Username: ")
        usernameTextBox = Entry(window, width=20)
        usernameTextBox.delete(0, END)

        passwordLabel = tkinter.Label(window, text="Password: ")
        passwordTextBox = Entry(window, width=20)
        passwordTextBox.delete(0, END)

        sendButton = Button(window, text = "Click here to finish", command = lambda: handleSendButton(window, usernameTextBox.get(), passwordTextBox.get()))

        usernameLabel.pack()        
        usernameTextBox.pack()     
        passwordLabel.pack()
        passwordTextBox.pack()
        sendButton.pack()

        window.protocol("WM_DELETE_WINDOW", lambda: handleAccountClosing(window))
        window.mainloop()

def handleSearchButton(window, cmd):
    send(cmd)
    global List 
    List = receiveList()
    print(List)

    tableList = st.ScrolledText(window, height = 10, width = 150)
    tableList.pack()

    for i in List:
        row = str(i)
        tableList.insert(END, row)
        tableList.insert(END, "\n")

    continueButton = Button(window, text = "Click here to continue searching", command = lambda: handleContinueButton(window))
    viewButton = Button(window, text = "Click here to View", command = lambda: handleViewButton(window))
    downloadButton = Button(window, text = "Click here to Download", command = lambda: handleDownloadButton(window))

    continueButton.pack()
    viewButton.pack()   
    downloadButton.pack()
    
def handleContinueButton(window):
    window.destroy()
    searchWindow()

def handleDownloadButton(window):
    send("DOWNLOAD")
    for i in List:
        fileName = receive()
        fileName = DOWNLOAD_PATH + "\\" + fileName
        receiveFile(fileName)
        fileName = ""
    print ("DOWNLOAD SUCCESSUL")


def viewWindow():
    window = Tk()
    window.title("Search information of book")
    window.geometry("1000x600")
    center(window)

    viewLabel = tkinter.Label(window, text="List of book you have search: ")
    table = st.ScrolledText(window, height = 100, width = 150)
    for i in List:
        data = receive()
        print (data + '\n')
        table.insert (END, "\n" + i["ID"] + " " + i["NAME"] + ":\n")
        table.insert (END, data)
        table.insert(END, "\n")

    viewLabel.pack()
    table.pack()

    #window.protocol("WM_DELETE_WINDOW", lambda: handleViewClosing(window))
    window.mainloop()

def handleViewButton(window):
    #window.destroy()
    send("VIEW")
    viewWindow()
    searchWindow()

def searchWindow():
    window = Tk()
    window.title("Search information of book")
    window.geometry("1000x600")

    searchLabel = tkinter.Label(window, text="Type here what you want to search: ")
    cmdTextBox = Entry(window, width = 100)
    searchButton = Button(window, text = "Click here to search", command = lambda: handleSearchButton(window, cmdTextBox.get()))

    searchLabel.pack(side = TOP)
    cmdTextBox.pack(side = TOP, fill = 'x')
    searchButton.pack()

    window.protocol("WM_DELETE_WINDOW", lambda: handleClosing(window))
    window.mainloop()

#main
try:
    choiceWindow()
except:
    exit()
