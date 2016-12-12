import socket
from thread import *
import string
import select,sys

#@PErintah
#----------------------------------------------FUNGSI - FUNGSI DARI PERINTAH CHAT SERVER----------------------------------------------------------------
def login(socket,username,password):#OK
    try:
        for i in range(0,len(ACCOUNT_LIST),1):
            if(i==(len(ACCOUNT_LIST)-1) and ACCOUNT_LIST[i][0]!=username and ACCOUNT_LIST[i][1]!=password):
                kirim_status(sock,2)            
            if(username==ACCOUNT_LIST[i][0] and password==ACCOUNT_LIST[i][1]):
                LOGIN_SESSION[CONNECTION_LIST.index(socket)]=username
                GROUP_SESSION[CONNECTION_LIST.index(socket)]="0"
                kirim_status(socket,1)
                break           
    except:
        kirim_status(socket,2)
        
def daftar(socket,username,password):#Ok
    try:
        for i in range(0,len(ACCOUNT_LIST),1):
            if(username==ACCOUNT_LIST[i][0] and password==ACCOUNT_LIST[i][1]):
                return
        f=open("akun_chat.txt","a+")
        f.write(username + " " + password +"\r\n")
        ACCOUNT_LIST.append([])
        ACCOUNT_LIST[(len(ACCOUNT_LIST))-1].append(username)
        ACCOUNT_LIST[(len(ACCOUNT_LIST))-1].append(password)
        f.close()
        kirim_status(socket,8)      
    except:
        kirim_status(socket,9)          
def keluar(socket):
    socket.close()
    CONNECTION_LIST.remove(socket)
def logout(socket):#OK
    try:
        LOGIN_SESSION[CONNECTION_LIST.index(socket)]="0"
        GROUP_SESSION[CONNECTION_LIST.index(socket)]="0"
        kirim_status(socket,6)              
    except:
        kirim_status(socket,7)              
def kirim_grup(sock,isipesan):#ok
    nama_grup=GROUP_SESSION[CONNECTION_LIST.index(sock)]
    #print(nama_grup)
    try :    
        for socket in CONNECTION_LIST:
            if (GROUP_SESSION[CONNECTION_LIST.index(socket)] == nama_grup and socket != sock) :
                socket.send(isipesan)              
        kirim_status(sock,3)                            
    except :
        kirim_status(socket,4)              
        socket.close()
        CONNECTION_LIST.remove(socket)

def kirim_private(sock,username_tujuan,isipesan):#ok
    try:
        flag=0
        for i in range(0, len(ACCOUNT_LIST), 1):
            if(username_tujuan==ACCOUNT_LIST[i][0]):
                tf=open("pesan.txt", "a+")
                baruisipesan=isipesan.replace("<","|")
                baruisipesan=baruisipesan.replace(">","|")
                tf.write(username_tujuan+baruisipesan)
                tf.close()
                kirim_status(sock,3)
                flag=1
                break
    except:
        kirim_status(sock,4)
def bgrup(sock,nama,password):
    try:
        for i in range(0,len(GROUP_LIST),1):
            if(nama==GROUP_LIST[i][0] and password==GROUP_LIST[i][1]):
                return
        fg=open("grup_chat.txt","a+")
        fg.write(nama + " " + password +"\r\n")
        GROUP_LIST.append([])
        GROUP_LIST[(len(GROUP_LIST))-1].append(nama)
        GROUP_LIST[(len(GROUP_LIST))-1].append(password)
        fg.close()
        kirim_status(sock,13)      
    except:
        kirim_status(sock,14)

def pgs(sock):#ok
    try:
    
        sock.send(GROUP_SESSION[CONNECTION_LIST.index(sock)]+"\r\n")
        kirim_status(sock,20)
    except:
        kirim_status(sock,21)    
def ggrup(sock,nama,password):#ok
    fg=open("grup_chat.txt","r")    
    try:    
        for line in fg:
            if(line==(nama+" "+password+'\n')):
                GROUP_SESSION[CONNECTION_LIST.index(sock)]=nama
                kirim_status(sock,12)
            
        fg.close()
    except:
        kirim_status(sock,15)
def tgrup(sock): #ok
    data=""
    try:
        for i in range(0,len(GROUP_LIST),1):
            data=data+str(i+1)+". "+ GROUP_LIST[i][0] +" \r\n"
        sock.send("\r\n"+data)
        kirim_status(sock,20)
    except:
        pkirim_status(sock,21)
def kgrup(sock):#ok
    try:
        GROUP_SESSION[CONNECTION_LIST.index(sock)]="0"
        kirim_status(sock,16)
    except:
        kirim_status(sock,17)
def hgrup(sock,nama,password):  
    try:
        fg=open("grup_chat.txt","r")    
        data=""
        for line in fg:
            if(line==(nama+" "+password+'\n')):
                continue
            data=data+line
       
        fg.close()   
        if data: 
        #HApus data grup di grup_chat.txt
            fg=open("grup_chat.txt","w")    
            fg.write(data)
            fg.close()
        #---------------------------------
        #Ubah default data grup di GROUP_SESSION
            for i in range(i,len(GROUP_SESSION),1):
                if GROUP_SESSION[i]==nama :
                    GROUP_SESSION[i]="0"
        #-------------------------------    
        #HApus data grup di GROUP_LIST
            for i in range(i,len(GROUP_LIST),1):
                if GROUP_LIST[i][0]==nama :
                    del GROUP_LIST[i]    
        kirim_status(sock,18)
    #-------------------------------    
    except :
        kirim_status(sock,19)
def apesan(socket):
    try:
        fp=open("pesan.txt", "r")
        #lines=fp.readlines()
        for line in fp:
            pesan=line.split("|")
            if(LOGIN_SESSION[CONNECTION_LIST.index(socket)]==pesan[0]):
                socket.send("<"+pesan[1]+">"+pesan[2])
        fp.close()
        fp=open("pesan.txt", "r")
        lines=fp.readlines()
        fp.close()
        fp=open("pesan.txt", "w")
        for line in lines:
            pesan=line.split("|")
            if(pesan[0]!=LOGIN_SESSION[CONNECTION_LIST.index(socket)]):
                fp.write(line)
        fp.close()
        kirim_status(sock,23)
    except:
        kirim_status(sock,24)
#@PEmrosesan
#----------------------------------------------FUNGSI - FUNGSI PEMROSESAN----------------------------------------------------------------
def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)              
            except :
                socket.close()
                CONNECTION_LIST.remove(socket)
#def is_user_terdaftar(username):
#    for

def kirim_status(conn,kode):
    if(kode == 1):
        deskripsi = str(kode)+ ":" +'Login Berhasil.'
    if(kode == 2):
        deskripsi = str(kode)+ ":" + 'Login Gagal.'
    if(kode == 3):
        deskripsi = str(kode)+ ":"  + 'Kirim Pesan Berhasil.'
    if(kode == 4):
        deskripsi = str(kode)+ ":"  + 'Kirim Pesan Gagal.'
    if(kode == 5):
        deskripsi = str(kode)+ ":"  + 'Proses Gagal,Karena Belum Terautentifikasi.'                         
    if(kode == 6):
        deskripsi = str(kode)+ ":"  + 'Logout Berhasil.'
    if(kode == 7):
        deskripsi = str(kode)+ ":"  + 'Logout Gagal.'
    if(kode == 8):
        deskripsi = str(kode)+ ":" + 'Daftar Berhasil.'
    if(kode == 9):
        deskripsi = str(kode)+ ":"  + 'Daftar Gagal.'
    if(kode == 10):
        deskripsi = str(kode)+ ":"  + 'Syntax Tidak Dikenali.'
    if(kode == 11):
        deskripsi = str(kode)+ ":"  + 'Join Chat Server Sukses.'                                
    if(kode == 12):
        deskripsi = "Gabung Grup "+GROUP_SESSION[CONNECTION_LIST.index(conn)]+ " Sukses."                            
    if(kode == 13):
        deskripsi =  str(kode)+ ":"  + 'Buat Grup Sukses.' 
    if(kode == 14):
        deskripsi =  str(kode)+ ":"  + 'Buat Grup Gagal.' 
    if(kode == 15):
        deskripsi =  str(kode)+ ":" + 'Gabung Grup Gagal.' 
    if(kode == 16):
        deskripsi =  str(kode)+ ":" + 'Keluar Grup Berhasil.' 
    if(kode == 17):
        deskripsi =  str(kode)+ ":" + 'Keluar Grup Gagal.' 
    if(kode == 18):
        deskripsi =  str(kode)+ ":" + 'Hapus Grup Berhasil.' 
    if(kode == 19):
        deskripsi =  str(kode)+ ":" + 'Hapus Grup Gagal.' 
    if(kode == 20):
        deskripsi =  str(kode)+ ":" + 'Data Berhasil Diterima.' 
    if(kode == 21):
        deskripsi =  str(kode)+ ":" + 'Data Gagal Diterima.' 
    if(kode == 22):
        deskripsi =  str(kode)+ ":" + 'Socket rusak.'
    if(kode == 23):
        deskripsi =  str(kode)+ ":" + 'Ambil pesan berhasil.'
    if(kode == 24):
        deskripsi =  str(kode)+ ":" + 'Ambil pesan gagal.'
    conn.send(deskripsi)
    
def menu_handling(sock):
    if sock == server_socket:
        koneksi_client,alamat_client= server_socket.accept()
        CONNECTION_LIST.append(koneksi_client)
        LOGIN_SESSION.append("0")
        GROUP_SESSION.append("0")        
        print "Koneksi dari ",alamat_client
        kirim_status(koneksi_client,11)                         
    else:
        # Data recieved from client, process it
        try:     
            message = sock.recv(1024)
            if message:
                perintah=message.split()      
                if(LOGIN_SESSION[CONNECTION_LIST.index(sock)]!="0"):            
                    #PErintah2 Yang PErlu AUtentifikasi                    
                    if (perintah[0].lower() == 'logout'):
                        logout(sock)                     
                    elif (perintah[0].lower() == 'kirim_private'):
                        kirim_private(sock,perintah[1],'<' + LOGIN_SESSION[CONNECTION_LIST.index(sock)] + '> ' + perintah[2] + "\r\n")                
                    elif (perintah[0].lower() == 'keluar'):
                        keluar(sock)                        
                    elif (perintah[0].lower() == 'bgrup'):
                        bgrup(sock,perintah[1],perintah[2])                   
                    elif (perintah[0].lower() == 'ggrup'):
                        ggrup(sock,perintah[1],perintah[2])
                    elif (perintah[0].lower() == 'tgrup'):
                        tgrup(sock)                  
                    elif (perintah[0].lower() == 'kgrup'):
                        kgrup(sock)      
                    elif (perintah[0].lower() == 'pgs'):
                        pgs(sock)                                                      
                    elif (perintah[0].lower() == 'hgrup'):
                        hgrup(sock,perintah[1],perintah[2])                    
                    elif (perintah[0].lower() == 'kirim_grup'):
                        kirim_grup(sock,'<' + LOGIN_SESSION[CONNECTION_LIST.index(sock)] + '> ' + perintah[1] + "\r\n")
                    elif (perintah[0].lower() == 'pgs'):
                        apesan(sock)
                    elif (perintah[0].lower() == 'apesan'):
                        apesan(sock)
                    else:
                        kirim_status(sock,10)
                else:
                    #PErintah2 TIdak PErlu Autentifikasi
                    if (perintah[0].lower() == 'login'):
                        login(sock,perintah[1],perintah[2])
                    elif (perintah[0].lower() == 'daftar'):
                        daftar(sock,perintah[1],perintah[2])
                    elif (perintah[0].lower() == 'logout' or perintah[0].lower() == 'kirim_private' or perintah[0].lower() == 'bgrup'or perintah[0].lower() == 'ggrup'or perintah[0].lower() == 'tgrup'or perintah[0].lower() == 'kgrup'or perintah[0].lower() == 'hgrup'or perintah[0].lower() == 'kirim_grup'):
                        kirim_status(sock,5)
                    elif (perintah[0].lower() == 'keluar'):                        
                        keluar(sock)
                    else:
                        kirim_status(sock,10)
        except:
                kirim_status(sock,22)
                sock.close()
                CONNECTION_LIST.remove(sock)

def inisialitation():
    # INsialisasi soket server
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(srver_address)
    server_socket.listen(10)
    CONNECTION_LIST.append(server_socket)
    LOGIN_SESSION.append("0")
    GROUP_SESSION.append("0")
    #--------------------------
    # Inisialisasi DAftar Akun
    f=open("akun_chat.txt","r")
    i=0    
    for line in f:
        akun=line.split()
        if akun:
            ACCOUNT_LIST.append([])
            ACCOUNT_LIST[i].append(akun[0])           
            ACCOUNT_LIST[i].append(akun[1])                   
            i=i+1
    f.close()
    #---------------------------                  
    # Inisialisasi DAftar Grup
    fg=open("grup_chat.txt","r")
    i=0    
    for line in fg:
        grup=line.split()
        if grup:
            GROUP_LIST.append([])
            GROUP_LIST[i].append(grup[0])           
            GROUP_LIST[i].append(grup[1])                   
            i=i+1
    fg.close()
    #---------------------------

#@Main
#----------------------------------------------FUNGSI MAIN----------------------------------------------------------------                
if __name__ == "__main__":
     
    CONNECTION_LIST = []    # DAftar PEngguna meliputi klien + server
    ACCOUNT_LIST=[]         #DAftar AKun dg Array 2d (kolom 1 username dan  kolom 2 password)
    GROUP_LIST=[]         #DAftar AKun dg Array 2d (kolom 1 nama grup dan  kolom 2 PAssword)
    LOGIN_SESSION=[]        #Loggin SEssion dg Array 1d(Isi nya adalah 0 untuk belum login dan selain 0(username) untuk yg sudah login)   
    GROUP_SESSION=[]         #Grup SEssion dg Array 1d(Isi nya adalah 0 untuk yg belumjoin dan selain 0(namagrup) untuk yg sudah join grup)   
    srver_address=("localhost", 10010) 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    green='\033[1;32m'
    blue = '\033[1;34m'
    red='\033[1;91m'
    yellow='\033[1;33m'
    underline = '\033[1;4m'    
    color_tail='\033[1;m'

    inisialitation()  
#    print (ACCOUNT_LIST)
    print "Dijalankan di interface %s port %s "%srver_address
    while True:
        print >> sys.stderr, 'Menunggu Koneksi'
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            menu_handling(sock)

     
    server_socket.close()

'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address=('127.0.0.1', 9011)
s.bind(address)
s.listen(10)
c = {} #isinya client
list_grup = list() #isinya list grup

def clientthread(conn):
    while 1:
        data = conn.recv(1024)
        e = data.split('>')

        #e [0] isinya username
        #perintah ada pada e [1]
        if len(e) == 3:
            if e[1] == 'BGRUP':
                try:
                    nama_grup = e[2]
                    if nama_grup == '':
                        data = 'beri nama grup dulu'
                    else:
                        nama_grup = e[2]
                        list_grup.append(nama_grup)
                        data = 'Grup berhasil dibuat'
                except:
                    data = 'grup belum memiliki nama'

            elif e[1] == 'TGRUP':
                if not list_grup:
                    data = 'belum ada grup'
                else:
                    for p in list_grup: data = p

            elif e[1] == 'TUTUP':
                break

            else:
                if e[1] == 'tampil':
                    try:
                        m = ''
                        for i in range(0, len(c[e[0]])):
                            m = m + c[e[0]][i]
                            if i != (len(c[e[0]])-1):
                                m = m + '\n'
                            if m == '':
                                data = 'pesan_kosong'
                            else:
                                data = m
                        del c[e[0]]
                    except:
                        data = 'pesan_kosong'
                else:
                    try:
                        c[e[1]]
                    except:
                        c[e[1]] = []
                        c[e[1]].append(e[0]+'>'+e[2])
                        data = 'Ok'

        #else if len(e) > 3:
        else:
            data = 'error'
        conn.send(data)
    conn.close()
    
while 1:
    conn, addr = s.accept()
    start_new_thread(clientthread ,(conn,))
    print 'ada koneksi'

s.close()
'''
