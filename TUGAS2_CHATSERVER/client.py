import socket
from thread import *
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8889))
u = raw_input('Username: ')

print 'To send: recipient>message'
def se(s):
    while 1:
        s.send(u + '>' + raw_input())
        print s.recv(1024)
def re(s):
    while 1:
        s.send(u + '>show>')
        r = s.recv(1024)
        if r != 'No messages':
            print r
        sleep(0.05)
start_new_thread(se ,(s,))
start_new_thread(re ,(s,))
while 1:
    pass
