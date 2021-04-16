from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter

from client import *

def handleChoiceClosing(window):
        send(DISCONNECT_MESSAGE)
        window.destroy()

def handleAccountClosing(window):
        send(DISCONNECT_MESSAGE)
        send(DISCONNECT_MESSAGE)
        window.destroy()

def handleLogInButton(window):
    send("LOG IN")
    window.withdraw() #hide ChoiceWindow
    inputAccountWindow()

def handleSignUpButton(window):
    send("SIGN UP")
    window.withdraw() #unhide choiceWindow
    inputAccountWindow()
    if inputAccountWindow.destroy():
        window.deiconify()

def choiceWindow():
    while True:
        global window
        window = Tk()
        window.title("Client's choice")
        window.geometry("500x500")

        logInButton = Button(window, text = "Click here to log in", command = lambda: handleLogInButton(window))
        logInButton.pack(fill = 'x')

        signUpButton = Button(window, text = "Click here to sign up", command = lambda: handleSignUpButton(window))
        signUpButton.pack(fill = 'x')

        #send !DISCONNECT message if client hit the exit button
        window.protocol("WM_DELETE_WINDOW", lambda: handleChoiceClosing)
        window.mainloop()

def handleSendButton(username, password):
    send(username)
    result = send(password)

    if result == "LOG IN SUCCEED":
        messagebox.showinfo("Notification", "Log in Successful")
    elif result == "LOG IN FAILED":
        messagebox.showinfo("Notification", "Username or Password is incorrect, try again")
    elif result == "SIGN UP SUCCEED":
        messagebox.showinfo("Notification", "Sign up Successful")
    elif result == "SIGN UP FAILED":
        messagebox.showinfo("Notification", "Username is used, try again")

def inputAccountWindow():
    window = Tk()
    window.title("Client's input")
    window.geometry("500x500")

    usernameLabel = tkinter.Label(window, text="Username: ")
    usernameLabel.pack()

    usernameTextBox = Entry(window, width=20)
    usernameTextBox.pack()

    passwordLabel = tkinter.Label(window, text="Password: ")
    passwordLabel.pack()

    passwordTextBox = Entry(window, width=20)
    passwordTextBox.pack()

    sendButton = Button(window, text = "Click here to finish", command = lambda: handleSendButton(usernameTextBox.get(), passwordTextBox.get()))
    sendButton.pack()

    window.protocol("WM_DELETE_WINDOW", lambda: handleAccountClosing(window))
    window.mainloop()

#main
choiceWindow()
