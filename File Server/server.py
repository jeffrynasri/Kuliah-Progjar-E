import socket
import sys
import os

def donwload(conn):
    filename='mytext.txt'
    f = open(filename,'rb')
    l = f.read(1024)
    while (l):
       conn.send(l)
       print('MEngirim ',repr(l))
       l = f.read(1024)
    f.close()

    print('Proses Download Sukses')
    conn.close()
def upload():
    print ("UPload")

def list():
    path = os.getcwd()
    dirs= os.listdir(path)
    for file in dirs:
        print file
        conn.sendall(file + "\r\n") 

def command_process(data):
    commands=data.split()
   # print (commands[0].lower())
    if (commands[0].lower() == 'list'):
        list()

def login_process():
    print ("login proses")
def command_menu():
    while True:
        conn.send(">> ")
        data = conn.recv(1024)
        if data:
               #print('Server received', repr(data))
            command_process(data)
        else:
            break
def login_menu():
    print("loginmenu")

    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 10000))           #DItempelkan di locahost port 10000
s.listen(1)                     

print 'Server listening....'
while True:
    conn, addr = s.accept()     # Membangun KOneksi denganklien
    try:
        print 'Ada Koneksi dari', addr
        command_menu()
    except KeyboardInterrupt:
        conn.close()
        sys.exit(0)
    finally:
        conn.close()
#    conn.close()
#    download_file(conn)
