import socket                   

def download_file(conn):
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

s = socket.socket()             # Inisialisasi Soket
s.bind(('localhost', 10000))           #DItempelkan di locahost port 10000
s.listen(1)                     

print 'Server listening....'

while True:
    conn, addr = s.accept()     # Membangun KOneksi dengan klien
    print 'Ada Koneksi dari', addr
    data = conn.recv(1024)
    print('Server received', repr(data))

    download_file(conn)
