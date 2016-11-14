import socket
from thread import *
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8889))
u = raw_input('Username: ')
p = raw_input('Password: ')

print 'Format pengiriman: recipient>message'

def kirim(s):
    while 1:
        s.send(u + '>' + raw_input())
        print s.recv(1024)
        
def terima(s):
    while 1:
        s.send(u + '>tampil>')
        r = s.recv(1024)
        if r != 'pesan_kosong':
            print r
        sleep(0.05)
        
start_new_thread(kirim ,(s,))
start_new_thread(terima ,(s,))
while 1:
    pass
