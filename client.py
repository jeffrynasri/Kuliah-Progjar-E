import socket                   # Import socket

s = socket.socket()             # Membuat soket

s.connect(('localhost', 10000))
s.send("Halo server!")

with open('file_download', 'wb') as f:
    print 'file terbuka'
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
