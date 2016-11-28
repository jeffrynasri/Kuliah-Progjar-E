import socket
from thread import *
#from time import sleep
import Tkinter

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.151.36.250", 10021))

#print 'Format pengiriman: recipient>message'
def kirim(s):
    top = Tkinter.Tk()
    while 1:
        command = raw_input()
        commands=command.split()
        if commands[0] == 'register':
            s.send(commands[0]+" "+commands[1]+" "+commands[2])
            r = s.recv(1024)
            print r
        elif commands[0] == 'login':
            s.send(commands[0]+" "+commands[1]+" "+commands[2])
            r = s.recv(1024)
            print r
        elif commands[0] == 'exit':
            s.close()
        elif commands[0] == 'send':
            s.send(commands[0]+" "+commands[1]+" "+commands[2])
            r = s.recv(1024)
            print r
        elif commands[0] == 'whoami':
            s.send(commands[0])
            r = s.recv(1024)
            print r
        elif commands[0] == 'online':
            s.send(commands[0])
            r = s.recv(1024)
            print r
        elif commands[0] == 'broadcast':
            s.send(commands[0]+" "+commands[1])
            r = s.recv(1024)
            print r
        elif commands[0] == 'checkpast':
            s.send(commands[0])
            r = s.recv(1024)
            print r
        elif commands[0] == 'check':
            s.send(commands[0])
            r = s.recv(1024)
            print r
        elif commands[0] == 'logout':
            s.send(commands[0])
            r = s.recv(1024)
            print r
        elif commands[0] == 'creategroup':
            s.send(commands[0]+" "+commands[1]+" "+commands[2])
            r = s.recv(1024)
            print r
        elif commands[0] == 'joingroup':
            s.send(commands[0]+" "+commands[1]+" "+commands[2])
            r = s.recv(1024)
            print r
        elif commands[0] == 'chatgroup':
            s.send(commands[0]+" "+commands[1]+" "+commands[2])
            r = s.recv(1024)
            print r
    top.mailoop()
'''def terima(s):
    while 1:
        s.send(u + '>tampil>')
        r = s.recv(1024)
        if r != 'pesan_kosong':
            print r
        sleep(0.05)'''
        
start_new_thread(kirim ,(s,))
#start_new_thread(terima ,(s,))
while 1:
    pass
