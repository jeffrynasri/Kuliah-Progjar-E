import socket
from thread import *
#from time import sleep
import Tkinter
from Tkinter import *
import tkMessageBox

def sequence(numb,window):
    if (numb==0):
        Login()
        MainMenu(window)
    elif (numb==1):
        Register()
        MainMenu(window)
    elif (numb==2):
        Exit()
        MainMenu(window)
        
def HomeMenu():
    window=Tkinter.Tk()
    
    loginbutton = Tkinter.Button(window, text="Login", command = lambda: Login(window))
    registerbutton = Tkinter.Button(window, text="Register", command = Register)
    exitbutton = Tkinter.Button(window, text="Exit", command = lambda: sequence(2,window))

    loginbutton.pack()
    registerbutton.pack()
    exitbutton.pack()
    window.mainloop()
    #return window

def MainMenu(window):
    window.destroy()
    window=Tkinter.Tk()
    
    window.mainLoop()
    
def Login(window):
    login=Tkinter.Tk()
    l1 = Label(login, text="User Name").grid(row=0, sticky=W)
    #l1.pack()
    e1 = Entry(login, bd =5)
    e1.grid(row=0, column=1)
    #e1.pack()
    l2 = Label(login, text="Password").grid(row=1, sticky=W)
    #l2.pack( side = LEFT)
    e2 = Entry(login, bd =5)
    e2.grid(row=1, column=1)
    #e2.pack(side = RIGHT)
    def callback():
        #s.send("Login "+e1.get()+" "+e2.get())
        #r = s.recv(1024)
        #print r
        tkMessageBox.showinfo("Info", e1.get()+" "+e2.get())
        login.destroy()
        MainMenu(window)
    okbutton = Tkinter.Button(login, text="Ok", command = callback).grid(row=2)
    login.mainloop()
    #tkMessageBox.showinfo("Info", "Ini Login")
    
def Register():
    register=Tkinter.Tk()
    l1 = Label(register, text="User Name").grid(row=0, sticky=W)
    e1 = Entry(register, bd =5)
    e1.grid(row=0, column=1)
    l2 = Label(register, text="Password").grid(row=1, sticky=W)
    e2 = Entry(register, bd =5)
    e2.grid(row=1, column=1)
    l3 = Label(register, text="Validasi Password").grid(row=2, sticky=W)
    e3 = Entry(register, bd =5)
    e3.grid(row=2, column=1)
    def callback():
        #s.send("Login "+e1.get()+" "+e2.get())
        #r = s.recv(1024)
        #print r
        tkMessageBox.showinfo("Info", e1.get()+" "+e2.get()+" "+e3.get())
        register.destroy()
        #MainMenu(window)
    okbutton = Tkinter.Button(register, text="Ok", command = callback).grid(row=3)
    register.mainloop()
    #tkMessageBox.showinfo("Info", "Ini Register")
    
def Exit():
    #s.send("Login "+e1.get()+" "+e2.get())
    #r = s.recv(1024)
    #print r
    tkMessageBox.showinfo("Info", "Ini Exit")

window=HomeMenu()
