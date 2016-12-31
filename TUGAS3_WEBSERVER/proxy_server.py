
import socket
import sys
import threading

#inisialisasi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#proses binding
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

#listening
sock.listen(1)

def http_get(message_yang_diteruskan, alamat):
    client_socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', alamat)
    client_socket.connect(server_address)
    try:
        # Kirim data
        message =  message_yang_diteruskan+"\r\n\r\n"
        #print >>sys.stderr, 'Message yang akan dikirim ' , message
        client_socket.sendall(message)
        data_respon = ""
        #baca data dari socket
        data_dari_server = client_socket.recv(32)
        while data_dari_server:
            data_respon = data_respon + data_dari_server
            data_dari_server = client_socket.recv(32)
            print >>sys.stderr, data_dari_server
    finally:
        return data_respon
        print >>sys.stderr, 'closing socket'
        client_socket.close()

def http_get(message_yang_diteruskan, alamat):
    client_socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_address = ('www.detik.com', 80)
    server_address = ('127.0.0.1', alamat)
    client_socket.connect(server_address)
    try:
        # Kirim data
        message =  message_yang_diteruskan+"\r\n\r\n"
        print >>sys.stderr, 'Message yang akan dikirim ' , message
        client_socket.sendall(message)
        data_respon = ""
        #baca data dari socket
        data_dari_server = client_socket.recv(32)
        while data_dari_server:
            data_respon = data_respon + data_dari_server
            data_dari_server = client_socket.recv(32)
            print >>sys.stderr, data_dari_server
    finally:
        return data_respon
        print >>sys.stderr, 'closing socket'
        client_socket.close()
        

#fungsi melayani client
def layani_client(koneksi_client,alamat_client):
    try:
        print >>sys.stderr, 'ada koneksi dari ', alamat_client
        request_message = ''
        while True:
            data = koneksi_client.recv(64)
            data = bytes.decode(data)
            request_message = request_message+data
            if (request_message[-4:]=="\r\n\r\n"):
                break

       #meneruskan request tersebut ke server yang dituju
        baris = request_message.split("\r\n")
        baris_request = baris[0]
        baris_host = baris[1]
        try :
            a,url,c = baris_request.split(" ")
            url, format = url.split(".")
            if(url=='/dokumen'):
                if format=='data':
                    alamat=11000
                    koneksi_keluar = http_get(request_message, alamat)
                if format=='html':
                    alamat=12000
                    koneksi_keluar = http_get(request_message, alamat)
                if format=='pdf':
                    alamat=13000
                    koneksi_keluar = http_get(request_message, alamat)
                if format=='txt':
                    alamat=14000
                    koneksi_keluar = http_get(request_message, alamat)
                respon = koneksi_keluar
        except:
            filedokumen = "File Tidak Ditemukan"
            panjang = len(filedokumen)
            hasil = "HTTP/1.1 404 Not Found\r\n" \
                    "Content-Type: text/html\r\n" \
                    "Content-Length: {}\r\n" \
                    "\r\n" \
                    "{}" . format(panjang, filedokumen)
            respon=hasil
           # print respon
        #    alamat=20000
        #    koneksi_keluar = http_get(request_message, alamat)
        #baca request headers
        #gunakan Host: untuk mendapatkan alamat yang harus di konek oleh socket
        
        
        koneksi_client.send(respon)
    finally:
        # Clean up the connection
        koneksi_client.close()


while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    koneksi_client, alamat_client = sock.accept()
    s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
    s.start()


