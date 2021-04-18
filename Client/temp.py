from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter


def handleSearchButton(cmd):
    numberOfResult = send(cmd)
    int(numberOfResult)
    send("number of result received")

    result = []
    for i in range(0, numberOfResult - 1):
        result.append(send("result received"))

def searchWindow():
    window = Tk()
    window.title("Search information of book")
    window.geometry("500x500")

    searchLabel = tkinter.Label(window, text="Type here what you want to search: ")
    searchLabel.pack(side = TOP)

    cmdTextBox = Entry(window, width = 100)
    cmdTextBox.pack(side = TOP, fill = 'x')

    searchButton = Button(window, text = "Click here to search", command = lambda: handleSearchButton(cmdTextBox.get()))
    searchButton.pack()

    listBox = Listbox()
    listBox.pack(fill = BOTH)

    window.protocol("WM_DELETE_WINDOW", lambda: handleClosing(window))
    window.mainloop()

#main
searchWindow()