
import socket
import sys
import threading

#inisialisasi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#proses binding
server_address = ('localhost', 11000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

#listening
sock.listen(1)

def http_get(message_yang_diteruskan,alamat):
	client_socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('www.detik.com', 80)
	client_socket.connect(server_address)
	try:
	    # Kirim data
	    message =  message_yang_diteruskan+"\r\n\r\n"
	    print >>sys.stderr, 'Nmessage yang akan dikirim ' , message
	    client_socket.sendall(message)
	    data_respon = ""
	    #baca data dari socket
	    while True:
		data_dari_server = client_socket.recv(32)
		data_respon = data_respon+data_dari_server
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
       #    print 'test'

       baris = request_message.split("\r\n")
       baris_request = baris[0]
       baris_host = baris[1]
       a,url,c = baris_request.split(" ")
       
       #baca request headers 
       #gunakan Host: untuk mendapatkan alamat yang harus di konek oleh socket

       #koneksi_keluar = http_get(request_message,alamat)
       #respon = koneksi_keluar
       #koneksi_client.send(respon)
    finally:
        # Clean up the connection
        koneksi_client.close()


while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    koneksi_client, alamat_client = sock.accept()
    s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
    s.start()


