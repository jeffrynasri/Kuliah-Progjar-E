import socket
import sys
import os
import time
import platform

host_server='127.0.0.1'
port_server = 10000
parent_dir='/home'
active_dir=os.getcwd()
rnfr_name=''

green='\033[1;32m'
blue = '\033[1;34m'
red='\033[1;91m'
yellow='\033[1;33m'
color_tail='\033[1;m'
#-------------------PROSES-PROSES FTP------------------------------
def retr(nama_file):
    global active_dir
    f = open(os.path.join(active_dir,nama_file),'rb')
    l = f.read(55524)
    while (l):
       conn.send(l)
       print('MEngirim ',repr(l))
       l = f.read(55524)
    f.close()
def stor(nama_file,isi):
    global active_dir
    f = open(os.path.join(active_dir,nama_file),'w+')
    l = f.write(isi)
    f.close()    

def list():
    global active_dir
    dirs= os.listdir(active_dir)
    for file in dirs:
        if(file.find('.')<0):
            file= blue + file + color_tail
        conn.sendall(file + "\r\n")   
def cwd(target):
    global active_dir
    if(target == '..'):
        (final, start)=os.path.split(active_dir)
        active_dir=final
    else:
        dir_list= os.listdir(active_dir)
        for dirr in dir_list:
            if(target == dirr):
                active_dir=os.path.join(active_dir,target)                                
                break
def pwd():
    global active_dir
    conn.sendall(active_dir + "\r\n") 
def dele(nama_file):
    os.remove(os.path.join(active_dir,nama_file))
def mkd(nama_dir):
    os.mkdir(os.path.join(active_dir,nama_dir))
def rmd(nama_dir):
    os.rmdir(os.path.join(active_dir,nama_dir))
def cdup():
    active_dir=parent_dir
def rnfr(nama_file):
    global rnfr_name
    rnfr_name=nama_file
    print(rnfr_name)
def rnto(nama_file):
    global active_dir
    if (rnfr_name == ''):
        status_send(450)
    else:
        os.rename(os.path.join(active_dir,rnfr_name),os.path.join(active_dir,nama_file))
def syst():
    conn.send("Remote system OS is "+platform.dist()[0]+" "+platform.dist()[1] + "\r\n")
def user(username):
    if(username == 'admin\r\n'):
        return 1
    else:
        return 0                    
def pass_(password):
    if(password == 'admin\r\n'):
        return 1
    else:
        return 0   
def quit():
    conn.close()
    sys.exit(0)
    print("OK")
def logout():
    active_dir=parent_dir
           
#--------------------------------------------------------------------

#------------------COmmand HAndle------------------------------------
def command_process(data):
    commands=data.split()
    if (commands[0].lower() == 'list'):
        list()
        status_send(250)
    if (commands[0].lower() == 'quit'):
        quit()
        status_send(221)
    if (commands[0].lower() == 'logout'):
        logout()        
        status_send(220)  
    if (commands[0].lower() == 'pwd'):
        pwd()                
        status_send(250)
    if (commands[0].lower() == 'cwd'):
        cwd(commands[1])                
        status_send(250)     
    if (commands[0].lower() == 'dele'):
        dele(commands[1])                
        status_send(250)   
    if (commands[0].lower() == 'mkd'):
        mkd(commands[1])                
        status_send(257)   
    if (commands[0].lower() == 'rmd'):
        rmd(commands[1])                
        status_send(250)
    if (commands[0].lower() == 'retr'):
        retr(commands[1])                
        status_send(250)
    if (commands[0].lower() == 'stor'):
        stor(commands[1],commands[2])                
#        status_send(226)  
    if (commands[0].lower() == 'cdup'):
        cdup()                
        status_send(250)
    if (commands[0].lower() == 'rnfr'):
        rnfr(commands[1])                
#        status_send(226)
    if (commands[0].lower() == 'rnto'):
        rnto(commands[1])                
#        status_send(226)
    if (commands[0].lower() == 'syst'):
        syst()                
        status_send(250)
    if (commands[0].lower() == 'noop'):               
        status_send(200)
    print("Ok")
def command_menu():
    while True:
        conn.send("[FTP-TC]"+ active_dir +">> ")
        data = conn.recv(1024)
        print(data)
        if data:
            command_process(data)
        if data.lower() == 'logout\r\n':
            break
    login_menu()            

def status_send(code):
    if(code == 150):
        description = green+ 'File Status Okay.'+ color_tail
    if(code == 200):
        description = green+ 'Command okay.'+ color_tail
    if(code == 212):
        description = blue + 'Directory status.' +color_tail 
    if(code == 215):
        description = blue + 'NAME system type.' +color_tail          
    if(code == 220):
        description = green+'Service ready for new user.' +color_tail     
    if(code == 221):
        description = green + 'Requested file succesfull.\r\nLogged out if appropriate.' +color_tail   
    if(code == 226):
        description = red + 'Service closing control connection.\r\nLogged out if appropriate.' +color_tail                          
    if(code == 230):
        description = green+ 'User logged in, proceed.'+ color_tail
    if(code == 250):
        description = green + 'Requested file action okay, completed.' + color_tail                             
    if(code == 257):
        description = green + '"PATHNAME" created.' +color_tail           
    if(code == 331):
        description = green + 'User name okay, need password.' +color_tail
    if(code == 332):
        description = red + 'Need account for login.' +color_tail      
    if(code == 500):
        description = red + 'Syntax error, command unrecognized.' +color_tail
    if(code == 501):
        description = red + 'Syntax error in parameters or arguments.' +color_tail                
    if(code == 530):
        description = red + 'Not logged in.' +color_tail
    if(code == 550):
        description = red + 'Requested action not taken.' +color_tail        
    conn.send(str(code) + " " + description + "\r\n")

#---------------------------------------------------------------------
#--------------------------LOGIN handle------------------------------

def login_menu():
    while True:
        conn.send("Username : ")
        username = conn.recv(1024)
        print(username.rstrip() + " mencoba login")
        if (user(username)):
            status_send(331)
        else:
            continue            
        conn.send("Password : ")
        password = conn.recv(1024)
        if (pass_(password)):
            print(username.rstrip() + "login pada " + time.asctime( time.localtime(time.time()) ) + " di " + host_server + ":"+str(port_server))
            status_send(230)
            conn.send ("Remote system OS is "+platform.dist()[0]+" "+platform.dist()[1] + "\r\n")
            break
        else:
            status_send(332)
    command_menu()            

#----------------------------------------------------------------

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host_server, port_server))
s.listen(1)                     

print 'Server listening....'

while True:
    conn, addr = s.accept()
    try:
        print 'Ada Koneksi dari', addr
        conn.send("-------FTP Server Kelompok 1-------\r\n")
        conn.send("       ---------------------       \r\n")
        conn.send("1. Jeffry Nasri Faruki 5114100043\r\n")        
        conn.send("2. R.AY. Noormal Nadya 5114100127\r\n")                
        conn.send("3. M Habibur Rahman 5114100163\r\n")
        conn.send("4. Kukuh Rilo Pambudi 5114100178\r\n")                                        
        conn.send("-----------------------------------\r\n")
        conn.send("Connected to ftp-progjarE-Kelompok1\r\n")

        status_send(220)
        login_menu()
#        command_menu()
    except KeyboardInterrupt:
        conn.close()
        sys.exit(0)
    finally:
        conn.close()

