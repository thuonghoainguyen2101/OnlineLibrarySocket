from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter

import json


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
    logInButton.pack(fill = 'x')

    signUpButton = Button(window, text = "Click here to sign up", command = lambda: handleSignUpButton(window))
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
        usernameLabel.pack()
        
        usernameTextBox = Entry(window, width=20)
        usernameTextBox.pack()
        usernameTextBox.delete(0, END)

        passwordLabel = tkinter.Label(window, text="Password: ")
        passwordLabel.pack()

        passwordTextBox = Entry(window, width=20)
        passwordTextBox.pack()
        passwordTextBox.delete(0, END)

        sendButton = Button(window, text = "Click here to finish", command = lambda: handleSendButton(window, usernameTextBox.get(), passwordTextBox.get()))
        sendButton.pack()

        window.protocol("WM_DELETE_WINDOW", lambda: handleAccountClosing(window))
        window.mainloop()

def handleSearchButton(window, cmd):
    send(cmd)
    List = receiveList()
    print(List)

    tableList = Text(window, height = 10, width = 150)
    tableList.pack()

    for i in List:
        row = str(i)
        tableList.insert(END, row)
        tableList.insert(END, "\n")

    continueButton = Button(window, text = "Click here to continue searching", command = lambda: handleContinueButton(window))
    continueButton.pack()
    
def handleContinueButton(window):
    window.destroy()
    searchWindow()

def searchWindow():
    window = Tk()
    window.title("Search information of book")
    window.geometry("1000x600")

    searchLabel = tkinter.Label(window, text="Type here what you want to search: ")
    searchLabel.pack(side = TOP)

    cmdTextBox = Entry(window, width = 100)
    cmdTextBox.pack(side = TOP, fill = 'x')

    searchButton = Button(window, text = "Click here to search", command = lambda: handleSearchButton(window, cmdTextBox.get()))
    searchButton.pack()

    window.protocol("WM_DELETE_WINDOW", lambda: handleClosing(window))
    window.mainloop()

#main
choiceWindow()
