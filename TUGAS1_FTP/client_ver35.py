import socket                   # Import socket

s = socket.socket()             # Membuat soket

s.connect(('localhost', 10000))
buat_send = 'Halo server'
s.send(buat_send.encode('utf-8'))

with open('file_download.txt', 'wb') as f:
    print ('file terbuka')
    while True:
        print('mendapatkan data...')
        data = s.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # menulis ke file
        f.write(data)

f.close()
print('Berhasil mendapatkan file')
s.close()
print('Koneksi ditutup')
