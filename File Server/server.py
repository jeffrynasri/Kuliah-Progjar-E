import socket
import sys
import os
import time

host_server='127.0.0.1'
port_server = 10000
parent_dir='\home'
active_dir=os.getcwd()

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
    
    print("OK")
    status_send(226)
def stor(nama_file):
    global active_dir
    print ("put=UPload")

def list():
    global active_dir
    dirs= os.listdir(active_dir)
    for file in dirs:
        if(file.find('.')<0):
            file= blue + file + color_tail
        conn.sendall(file + "\r\n") 
    print("OK")        
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
    print("OK")            

def pwd():
    global active_dir
    conn.sendall(active_dir + "\r\n") 
    print("OK")    
def dele(nama_file):
    os.remove(os.path.join(active_dir,nama_file))
    print("OK")    
def mkd(nama_dir):
    os.mkdir(os.path.join(active_dir,nama_dir))
    print("OK")    
def rmd(nama_dir):
    os.rmdir(os.path.join(active_dir,nama_dir))
    print("OK")
def cdup(nama_dir):
  #  os.mkdir(os.path.join(active_dir,nama_dir))
    print("OK")    
def rnfr(nama_dir):
  #  os.mkdir(os.path.join(active_dir,nama_dir))
    print("OK")   
def rnto(nama_dir):
  #  os.mkdir(os.path.join(active_dir,nama_dir))
    print("OK")    
def syst(nama_dir):
  #  os.mkdir(os.path.join(active_dir,nama_dir))
    print("OK")   
def noop(nama_dir):
  #  os.mkdir(os.path.join(active_dir,nama_dir))
    print("OK") 
def user(nama_dir):
  #  os.mkdir(os.path.join(active_dir,nama_dir))
    print("OK")                      
def pass(nama_dir):
  #  os.mkdir(os.path.join(active_dir,nama_dir))
    print("OK")     
def quit():
    conn.close()
    sys.exit(0)
    print("OK")
def logout():
    active_dir=parent_dir
    print("OK")
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
    if (commands[0].lower() == 'pwd'):
        pwd()                
        status_send(226)
    if (commands[0].lower() == 'cd'):
        cd(commands[1])                
#        status_send(226)     
    if (commands[0].lower() == 'delete'):
        delete(commands[1])                
#        status_send(226)   
    if (commands[0].lower() == 'mkdir'):
        mkdir(commands[1])                
#        status_send(226)   
    if (commands[0].lower() == 'rmdir'):
        rmdir(commands[1])                
#        status_send(226)
    if (commands[0].lower() == 'get'):
        get(commands[1])                
#        status_send(226)    
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
    if(code == 200):
        description = green+ 'Command okay.'+ color_tail
    if(code == 212):
        description = red + 'Directory status.' +color_tail 
    if(code == 215):
        description = red + 'NAME system type.' +color_tail          
    if(code == 220):
        description = green+'Service ready for new user.' +color_tail     
    if(code == 221):
        description = red + 'Service closing control connection.\r\nLogged out if appropriate.' +color_tail                   
    if(code == 230):
        description = green+ 'User logged in, proceed.'+ color_tail
    if(code == 250):
        description = green + 'Requested file action okay, completed.' + color_tail                             
    if(code == 257):
        description = red + '"PATHNAME" created.' +color_tail           
    if(code == 331):
        description = red + 'User name okay, need password.' +color_tail
    if(code == 332):
        description = red + 'Need account for login.' +color_tail      
    if(code == 500):
        description = red + 'Syntax error, command unrecognized.' +color_tail
    if(code == 501):
        description = red + 'Syntax error in parameters or arguments.' +color_tail                
    if(code == 530):
        description = red + 'Not logged in.' +color_tail
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
            print(username.rstrip() + " mencoba login")
            if(login_process(username,password) == 1):
                print(username.rstrip() + "login pada " + time.asctime( time.localtime(time.time()) ) + " di " + host_server + ":"+str(port_server))
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
s.bind((host_server, port_server))
s.listen(1)                     

print 'Server listening....'

while True:
    conn, addr = s.accept()     # Membangun KOneksi denganklien
    try:
        print 'Ada Koneksi dari', addr
        conn.send("-------FTP Server Kelompok 1-------\r\n")
        conn.send("       ---------------------       \r\n")
        conn.send("1. Jeffry Nasri Faruki 5114100043\r\n")        
        conn.send("2. R.AY. Noormal Nadya 5114100127\r\n")                
        conn.send("3. M Habibur Rahman 5114100163\r\n")
        conn.send("4. Kukuh Rilo Pambudi 5114100178\r\n")                                        
        conn.send("-----------------------------------\r\n")
        conn.send("Tersambung Ke FTP Server Kelompok 1\r\n")

        status_send(220)
        login_menu()
#        command_menu()
    except KeyboardInterrupt:
        conn.close()
        sys.exit(0)
    finally:
        conn.close()

