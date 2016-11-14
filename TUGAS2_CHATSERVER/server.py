import socket
from thread import *
import string

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
