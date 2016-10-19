import socket
import sys
import os

#-------------------PROSES-PROSES FTP------------------------------
def get(conn):
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
def put():
    print ("put=UPload")

def ls():
    path = os.getcwd()
    dirs= os.listdir(path)
    for file in dirs:
        print file
        conn.sendall(file + "\r\n") 
def cd():
    print ("INi CD")        

def delete():
    print ("DElete") 
def mkdir():
    print ("mkdir")     
def rmdir():
    print ("rmdir")
def quit():
    conn.close()
    sys.exit(0)
def logout():
    status_send(220)             
#--------------------------------------------------------------------

#------------------COmmand HAndle------------------------------------
def command_process(data):
    commands=data.split()
    if (commands[0].lower() == 'ls'):
        ls()
        status_send(226)
    if (commands[0].lower() == 'quit'):
        status_send(221)
        quit()
    if (commands[0].lower() == 'logout'):
        status_send(231)
        logout()                
def command_menu():
    while True:
        conn.send("[FTP-TC]>> ")
        data = conn.recv(1024)
        if data:
            command_process(data)
        if data.lower() == 'logout\r\n':
            break
    login_menu()            

def status_send(code):
    if(code == 230):
        description = 'Login Sukses'
    if(code == 231):
        description = 'Logout Sukses'
    if(code == 220):
        description = 'FTP Server Ready!'   
    if(code == 250):
        description = 'Perintah CWD Sukses'                             
    if(code == 221):
        description = 'Menutup FTP Server' 
    if(code == 226):
        description = 'Kirim Data Sukses'         
    if(code == 530):
        description = 'Belum Login'
    conn.send(str(code) + " " + description + "\r\n")
#---------------------------------------------------------------------
#--------------------------LOGIN handle------------------------------
def login_process(username,password):
    if(username == 'admin\r\n' and password == 'admin\r\n'):
        return 1
    else:
        return 0

def login_menu():
    while True:
        conn.send("Username : ")
        username = conn.recv(1024)
        conn.send("Password : ")
        password = conn.recv(1024)
        if username and password:
               #print('Server received', repr(data))
            if(login_process(username,password) == 1):
                print ("1")
                break
            else:
                status_send(530)                
        else:
            status_send(530)
    status_send(230)            
    command_menu()            

#----------------------------------------------------------------

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 10000))
s.listen(1)                     

print 'Server listening....'

while True:
    conn, addr = s.accept()     # Membangun KOneksi denganklien
    try:
        print 'Ada Koneksi dari', addr
        conn.send("Tersambung Ke FTP Server Kelompok 1\r\n")
        status_send(220)
        login_menu()
    except KeyboardInterrupt:
        conn.close()
        sys.exit(0)
    finally:
        conn.close()
#    conn.close()
#    download_file(conn)
