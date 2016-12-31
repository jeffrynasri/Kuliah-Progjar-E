
import socket
import sys
import threading

#inisialisasi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#proses binding
server_address = ('localhost', 11000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

#listening
sock.listen(1)

def response_data():
	filedokumen = open('dokumen.data','r').read()
	panjang = len(filedokumen)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, filedokumen)
	return hasil

def response_error():
	filedokumen = "File Tidak Ditemukan"
	panjang = len(filedokumen)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, filedokumen)
	return hasil

def response_icon():
	filegambar = open('myicon.png','r').read()
	panjang = len(filegambar)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: image/png\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, filegambar)
	return hasil


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

		baris = request_message.split("\r\n")
		baris_request = baris[0]
       #print baris_request
 	
		a,url,c = baris_request.split(" ")
       
		if (url=='/favicon.ico'):
			respon = response_icon()
		elif (url=='/dokumen.data'):
			respon = response_data()
		else:
			respon = response_error()
		
		print respon
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


