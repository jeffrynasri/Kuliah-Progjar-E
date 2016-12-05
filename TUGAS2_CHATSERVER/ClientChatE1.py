from Tkinter import *
import sys
import socket
import select
import tkMessageBox

WIDTH_DEFAULT=500
HEIGHT_DEFAULT=600
#host="10.151.36.250"
#port=10020
host="127.0.0.1"
port=10020
user_login=""
callback=None

def center_windows_position(BaseWindows):
	ws = BaseWindows.winfo_screenwidth() # width of the screen
	hs = BaseWindows.winfo_screenheight() # height of the screen
	x = (ws/2) - (WIDTH_DEFAULT/2)
	y = (hs/2) - (HEIGHT_DEFAULT/2)
	BaseWindows.geometry('%dx%d+%d+%d' % (WIDTH_DEFAULT,HEIGHT_DEFAULT, x, y))
	BaseWindows.geometry(str(WIDTH_DEFAULT)+"x"+str(HEIGHT_DEFAULT))
def draw_tittle(BaseWindows):
	global user_login
	frame_judul = Frame(BaseWindows,bg="#657D7F")
	frame_judul.pack(fill=X)
	if not user_login:
		judul=Label(frame_judul, text="ChatClient-E1 ", font=("Helvetica", 24,"bold underline"),bg="#657D7F")
	else:
		judul=Label(frame_judul, text="ChatClient-E1 ("+user_login+")", font=("Helvetica", 20,"bold underline"),bg="#657D7F")
	judul.pack(side=TOP,expand=TRUE,fill=X,pady=20)
def clear_frame(BaseWindows):
	for Frame in BaseWindows.winfo_children():
		Frame.destroy()
def show_status_code(code):
	if str(code)=="100":		
		tkMessageBox.showinfo("Status Kode", str(code)+":Sukses")
	elif str(code)=="200":		
		tkMessageBox.showerror("Status Kode", str(code)+":Gagal Command Tidak Dikenal")		
	elif str(code)=="210":		
		tkMessageBox.showerror("Status Kode", str(code)+":Syntax Error")
	elif str(code)=="220":		
		tkMessageBox.showerror("Status Kode", str(code)+":Autentifikasi Error")		
	elif str(code)=="230":		
		tkMessageBox.showerror("Status Kode", str(code)+":Registrasi Error")
	elif str(code)=="231":		
		tkMessageBox.showerror("Status Kode", str(code)+":Username Terpakai")		
	elif str(code)=="232":		
		tkMessageBox.showerror("Status Kode", str(code)+":Confirm Password Error")
	elif str(code)=="241":		
		tkMessageBox.showerror("Status Kode", str(code)+":Username Tidak Tersedia")
		print("asd")
	elif str(code)=="242":		
		tkMessageBox.showerror("Status Kode", str(code)+":Password Salah")
	elif str(code)=="243":		
		tkMessageBox.showerror("Status Kode", str(code)+":Username Sedang Online")		
	elif str(code)=="251":		
		tkMessageBox.showerror("Status Kode", str(code)+":Penerima Tidak Terdaftar")
	elif str(code)=="261":		
		tkMessageBox.showerror("Status Kode", str(code)+":Nama Grup Tidak Terdaftar")		
	elif str(code)=="271":		
		tkMessageBox.showerror("Status Kode", str(code)+":Nama Grup Telah Terpakai")
	elif str(code)=="281":		
		tkMessageBox.showerror("Status Kode", str(code)+":Grup Tidak Ada")		
	elif str(code)=="282":		
		tkMessageBox.showerror("Status Kode", str(code)+":Belum Tergabung Dalam Grup")
	elif str(code)=="291":		
		tkMessageBox.showerror("Status Kode", str(code)+":Sudah Menjadi Anggota Group")
	elif str(code)=="292":		
		tkMessageBox.showerror("Status Kode", str(code)+":Password Grup Salah")
	elif str(code)=="293":		
		tkMessageBox.showerror("Status Kode", str(code)+":Group Tidak Ada")				

def MenuLogin(BaseWindows):
	clear_frame(BaseWindows)
	BaseWindows.title("Aplikasi Chat Clien")
	BaseWindows.minsize(WIDTH_DEFAULT,HEIGHT_DEFAULT)
	BaseWindows.maxsize(WIDTH_DEFAULT,HEIGHT_DEFAULT)   
	center_windows_position(BaseWindows)
	draw_tittle(BaseWindows)
	
	frame_login = Frame(BaseWindows)
	frame_login.pack(fill=X)
	lbl_username = Label(frame_login, text="Username", width=11)
	lbl_username.pack(side=LEFT)
	entry_username=Entry(frame_login,textvariable=StringVar(frame_login, value="tion"))
	entry_username.pack(side=RIGHT,fill=X,pady=10, padx=10,expand=True)
	
	frame_login2 = Frame(BaseWindows)
	frame_login2.pack(fill=X)
	lbl_password = Label(frame_login2, text="Password", width=11)
	lbl_password.pack(side=LEFT)
	entry_password=Entry(frame_login2,textvariable=StringVar(frame_login2, value="789"))
	entry_password.pack(side=LEFT,fill=X,pady=10, padx=10,expand=True)
	
	frame_button = Frame(BaseWindows)
	frame_button.pack(fill=X)
	button_login = Button(frame_button, text ="Login", command = lambda: login(BaseWindows))
	button_login.pack(fill=X,pady=10, padx=10,expand=True)
	button_register = Button(frame_button, text ="Register", command = lambda: MenuRegister(BaseWindows))
	button_register.pack(fill=X,pady=10, padx=10,expand=True)
def MenuRegister(BaseWindows):
	clear_frame(BaseWindows)
	frame_back = Frame(BaseWindows)
	frame_back.pack(fill=X)
	button_back = Button(frame_back, text ="Kembali", command = lambda: MenuLogin(BaseWindows))
	button_back.pack(side=LEFT,fill=X,pady=10, padx=10)
	draw_tittle(BaseWindows)
	
	frame_register = Frame(BaseWindows)
	frame_register.pack(fill=X)
	lbl_username = Label(frame_register, text="Username", width=11)
	lbl_username.pack(side=LEFT)
	entry_username=Entry(frame_register)
	entry_username.pack(side=RIGHT,fill=X,pady=10, padx=10,expand=True)
	
	frame_register2 = Frame(BaseWindows)
	frame_register2.pack(fill=X)
	lbl_password = Label(frame_register2, text="Password", width=11)
	lbl_password.pack(side=LEFT)
	entry_password=Entry(frame_register2)
	entry_password.pack(side=LEFT,fill=X,pady=10, padx=10,expand=True)
	
	frame_register3 = Frame(BaseWindows)
	frame_register3.pack(fill=X)
	lbl_password = Label(frame_register3, text="Password Again", width=11)
	lbl_password.pack(side=LEFT)
	entry_password=Entry(frame_register3)
	entry_password.pack(side=LEFT,fill=X,pady=10, padx=10,expand=True)
	
	frame_button = Frame(BaseWindows)
	frame_button.pack(fill=X)
	button_register = Button(frame_button, text ="Register", command = lambda: register(BaseWindows))
	button_register.pack(fill=X,pady=10, padx=10,expand=True)
def MenuHome(BaseWindows):
	clear_frame(BaseWindows)
	draw_tittle(BaseWindows)
	#BaseWindows.minsize(WIDTH_DEFAULT,HEIGHT_DEFAULT)
	#BaseWindows.maxsize(WIDTH_DEFAULT,HEIGHT_DEFAULT)
	frame_toolbar=Frame(BaseWindows,bd=1,relief=RAISED)
	frame_toolbar.pack(side=TOP,fill=X)
	button_pm = Button(frame_toolbar,text="PM",command=lambda: MenuPM(BaseWindows))
	button_pm.pack(side=LEFT, padx=2, pady=2)
	button_broadcast = Button(frame_toolbar,text="Broadcast",command=lambda: MenuBroadcast(BaseWindows))
	button_broadcast.pack(side=LEFT, padx=2, pady=2)
	button_creategroup = Button(frame_toolbar,text="Create Group",command=lambda: MenuCreateGroup(BaseWindows))
	button_creategroup.pack(side=LEFT, padx=2, pady=2)
	button_join = Button(frame_toolbar,text="Join Group",command=lambda: MenuJoin(BaseWindows))
	button_join.pack(side=LEFT, padx=2, pady=2)
	button_chatgroup = Button(frame_toolbar,text="Chat Group",command=lambda: MenuChatGroup(BaseWindows))
	button_chatgroup.pack(side=LEFT, padx=2, pady=2)
	button_logout = Button(frame_toolbar,text="Logout",command=lambda: logout(BaseWindows))
	button_logout.pack(side=LEFT, padx=2, pady=2)
	
	frame_inbox = Frame(BaseWindows)
	frame_inbox.pack(fill=X)
	label_inbox = Label(frame_inbox, text="Inbox",  font=("Helvetica", 16,"bold"))
	label_inbox.pack(fill=X,expand=True)
	listbox_inbox=Listbox(frame_inbox,bg="white",fg="green",height=23)
	#scrollbar = Scrollbar(listbox_inbox)
	#listbox_inbox.config(yscrollcommand=scrollbar.set)
	#scrollbar.config(command=listbox_inbox.yview)
	#crollbar.pack(side=RIGHT)
	#listbox_inbox.config(height=23)
	listbox_inbox.pack(fill=X, pady=10, padx=10,expand=True)
	listbox_inbox.bind('<Double-Button-1>',listbox_detail)
	s.sendall("checkpast")
	check_past(BaseWindows)
	button_refresh = Button(frame_inbox,text="Refresh",command=lambda: refresh(BaseWindows,0))
	button_refresh.pack(padx=10, pady=10)
        
def MenuPM(BaseWindows):
	clear_frame(BaseWindows)
	frame_back = Frame(BaseWindows)
	frame_back.pack(fill=X)
	button_back = Button(frame_back, text ="Kembali", command = lambda: MenuHome(BaseWindows))
	button_back.pack(side=LEFT,fill=X,pady=10, padx=10)
	
	draw_tittle(BaseWindows)
	
	frame_user=Frame(BaseWindows)
	frame_user.pack(fill=X)
	label_user=Label(frame_user,text="Daftar User Online")
	label_user.pack(side=LEFT,fill=X,pady=10,padx=10,expand=True)
	listbox_user=Listbox(frame_user,selectmode=SINGLE)
	listbox_user.pack(fill=X,pady=10,padx=10,expand=True)
	s.sendall("online")
	online(BaseWindows)
	
	frame_usert=Frame(BaseWindows)
	frame_usert.pack(fill=X)
	label_tujuan=Label(frame_usert,text="Username Tujuan")
	label_tujuan.pack(side=LEFT,fill=X,padx=10,pady=10,expand=True)
	entry_username=Entry(frame_usert)
	entry_username.pack(fill=X,padx=10,pady=10,expand=True)
	
	frame_pesan=Frame(BaseWindows)
	frame_pesan.pack(fill=X)
	label_pesan=Label(frame_pesan,text="Pesan")
	label_pesan.pack(side=LEFT,fill=X,pady=10,padx=10,expand=True)
	entry_pesan=Entry(frame_pesan)
	entry_pesan.pack(fill=X,padx=10,pady=10,expand=True)
	
	frame_button=Frame(BaseWindows)
	frame_button.pack(fill=X)
	button_send=Button(frame_button,text="SEND", command = lambda: send(BaseWindows))
	button_send.pack(fill=X,padx=10,pady=10)
	
def MenuBroadcast(BaseWindows):
	clear_frame(BaseWindows)
	frame_back = Frame(BaseWindows)
	frame_back.pack(fill=X)
	button_back = Button(frame_back, text ="Kembali", command = lambda: MenuHome(BaseWindows))
	button_back.pack(side=LEFT,fill=X,pady=10, padx=10)
	
	draw_tittle(BaseWindows)
	
	frame_broadcast=Frame(BaseWindows)
	frame_broadcast.pack(fill=X)
	entry_broadcast=Entry(frame_broadcast,textvariable=StringVar(frame_broadcast, value="Pesan"))
	entry_broadcast.pack(fill=X,padx=10,pady=10,expand=True)
	label_keterangan=Label(frame_broadcast,text="Ket : Broadcast adalah mengirim pesan ke semua user")
	label_keterangan.pack(fill=X,pady=10,padx=10,expand=True)
	button_broadcast=Button(frame_broadcast,text="BROADCAST", command = lambda: broadcast(BaseWindows))
	button_broadcast.pack(fill=X,padx=10,pady=10)
	
	
def MenuCreateGroup(BaseWindows):
	clear_frame(BaseWindows)
	frame_back = Frame(BaseWindows)
	frame_back.pack(fill=X)
	button_back = Button(frame_back, text ="Kembali", command = lambda: MenuHome(BaseWindows))
	button_back.pack(side=LEFT,fill=X,pady=10, padx=10)
	draw_tittle(BaseWindows)
	
	frame_creategroup = Frame(BaseWindows)
	frame_creategroup.pack(fill=X)
	lbl_name = Label(frame_creategroup, text="Nama Grup", width=11)
	lbl_name.pack(side=LEFT)
	entry_name=Entry(frame_creategroup)
	entry_name.pack(side=RIGHT,fill=X,pady=10, padx=10,expand=True)
	
	frame_creategroup2 = Frame(BaseWindows)
	frame_creategroup2.pack(fill=X)
	lbl_password = Label(frame_creategroup2, text="Password", width=11)
	lbl_password.pack(side=LEFT)
	entry_password=Entry(frame_creategroup2)
	entry_password.pack(side=LEFT,fill=X,pady=10, padx=10,expand=True)
	
	frame_button = Frame(BaseWindows)
	frame_button.pack(fill=X)
	button_create = Button(frame_button, text ="CREATE GROUP", command = lambda: creategroup(BaseWindows))
	button_create.pack(fill=X,pady=10, padx=10,expand=True)			
def MenuJoin(BaseWindows):
	clear_frame(BaseWindows)
	frame_back = Frame(BaseWindows)
	frame_back.pack(fill=X)
	button_back = Button(frame_back, text ="Kembali", command = lambda: MenuHome(BaseWindows))
	button_back.pack(side=LEFT,fill=X,pady=10, padx=10)
	
	draw_tittle(BaseWindows)
	
	##frame_group=Frame(BaseWindows)
	##frame_group.pack(fill=X)
	#label_group=Label(frame_group,text="Daftar Grup")
	#label_group.pack(side=LEFT,fill=X,pady=10,padx=10,expand=True)
	#listbox_group=Listbox(frame_group,selectmode=SINGLE)
	#listbox_group.pack(fill=X,pady=10,padx=10,expand=True)
	
	frame_join=Frame(BaseWindows)
	frame_join.pack(fill=X)
	label_groupt=Label(frame_join,text="Nama Group")
	label_groupt.pack(side=LEFT,fill=X,pady=10,padx=10,expand=True)
	entry_group=Entry(frame_join)
	entry_group.pack(fill=X,padx=10,pady=10,expand=True)
	
	frame_join2=Frame(BaseWindows)
	frame_join2.pack(fill=X)
	label_password=Label(frame_join2,text="Password Group")
	label_password.pack(side=LEFT,fill=X,pady=10,padx=10,expand=True)
	entry_password=Entry(frame_join2)
	entry_password.pack(fill=X,padx=10,pady=10,expand=True)
	
	frame_buttonjoin=Frame(BaseWindows)
	frame_buttonjoin.pack(fill=X)
	button_join=Button(frame_buttonjoin,text="JOIN GRUP", command = lambda: joingroup(BaseWindows))
	button_join.pack(fill=X,padx=10,pady=10,expand=True)	
def MenuChatGroup(BaseWindows):
	clear_frame(BaseWindows)
	frame_back = Frame(BaseWindows)
	frame_back.pack(fill=X)
	button_back = Button(frame_back, text ="Kembali", command = lambda: MenuHome(BaseWindows))
	button_back.pack(side=LEFT,fill=X,pady=10, padx=10)
	
	draw_tittle(BaseWindows)
	
	#frame_group=Frame(BaseWindows)
	#frame_group.pack(fill=X)
	#label_group=Label(frame_group,text="Daftar Grup")
	#label_group.pack(side=LEFT,fill=X,pady=10,padx=10,expand=True)
	#listbox_group=Listbox(frame_group,selectmode=SINGLE)
	#listbox_group.pack(fill=X,pady=10,padx=10,expand=True)
	
	frame_chatg=Frame(BaseWindows)
	frame_chatg.pack(fill=X)
	label_groupt=Label(frame_chatg,text="Nama Group")
	label_groupt.pack(side=LEFT,fill=X,pady=10,padx=10,expand=True)
	entry_group=Entry(frame_chatg)
	entry_group.pack(fill=X,padx=10,pady=10,expand=True)
	
	frame_chatg2=Frame(BaseWindows)
	frame_chatg2.pack(fill=X)
	label_pesan=Label(frame_chatg2,text="Pesan")
	label_pesan.pack(side=LEFT,fill=X,pady=10,padx=10,expand=True)
	entry_pesan=Entry(frame_chatg2)
	entry_pesan.pack(fill=X,padx=10,pady=10,expand=True)
	
	frame_buttonchatg=Frame(BaseWindows)
	frame_buttonchatg.pack(fill=X)
	button_chatg=Button(frame_buttonchatg,text="CHAT GRUP", command = lambda: chatgroup(BaseWindows))
	button_chatg.pack(fill=X,padx=10,pady=10,expand=True)			
def connect_server():
	try :
		s.connect((host,port))
	except Exception as e :
		tkMessageBox.showerror("Error", str(e))
def online(BaseWindows):
	try:
		rdata = s.recv(2048)
		if not rdata:
			BaseWindows.after_cancel(callback)
		elif rdata:
			#daftar_user.append(rdata)
			datas=rdata.split("\n")
			Frame=BaseWindows.winfo_children()
			widgets = Frame[2].winfo_children()
			for data in datas:
				if not data:
					continue
				elif str(data)=="SUKSES 100":
					continue
				else:
					widgets[1].insert(END,data)
			callback=BaseWindows.after(1000,online(BaseWindows))
	except:
		callback=0
		print("DAftar USer DIdapatkan")
			
def login(BaseWindows):
	Frame=BaseWindows.winfo_children()
	widgets = Frame[1].winfo_children()
	username= str(widgets[1].get())
	widgets = Frame[2].winfo_children()
	password= str(widgets[1].get())
	s.sendall("login "+username+" "+password)
	terima=s.recv(4096)
	status_kode=terima.split()
	show_status_code(status_kode[1])
	
	if (str(status_kode[1])=="100"):
		global user_login
		user_login=username
		MenuHome(BaseWindows)
def listbox_detail(evt):
	w = evt.widget
	index = int(w.curselection()[0])
	value = w.get(index)
	data=value.split(" ")
	
	tanggal=data[0]
	waktu=data[1]
	data2=data[2].split(":")
	if (len(data2)==1):
		jenis="Private Message"
		pengirim=data2[0]
	else:
		if(data2[0] == "broadcast"):
			jenis=data2[0]
			pengirim=data2[1]
		else:
			jenis="Grup "+data2[0]
			pengirim=data2[1]
	isi=""
	for i in range(3,len(data),1):
		isi=isi+" "+data[i]

	listbox_detailWindows = Tk()		
	listbox_detailWindows.title("Detail Pesan")
	center_windows_position(listbox_detailWindows)
	
	frame_tanggal = Frame(listbox_detailWindows)
	frame_tanggal.pack(fill=X)
	lbl_tanggal = Label(frame_tanggal, text="Tanggal", width=11)
	lbl_tanggal.pack(side=LEFT)
	entry_tanggal=Entry(frame_tanggal,textvariable=StringVar(frame_tanggal, value=tanggal))
	entry_tanggal.pack(side=RIGHT,fill=X,pady=10, padx=10,expand=True)
	
	frame_waktu = Frame(listbox_detailWindows)
	frame_waktu.pack(fill=X)
	lbl_waktu = Label(frame_waktu, text="Waktu", width=11)
	lbl_waktu.pack(side=LEFT)
	entry_waktu=Entry(frame_waktu,textvariable=StringVar(frame_waktu, value=waktu))
	entry_waktu.pack(side=RIGHT,fill=X,pady=10, padx=10,expand=True)
	
	frame_jenis = Frame(listbox_detailWindows)
	frame_jenis.pack(fill=X)
	lbl_jenis = Label(frame_jenis, text="Jenis Pesan", width=11)
	lbl_jenis.pack(side=LEFT)
	entry_jenis=Entry(frame_jenis,textvariable=StringVar(frame_jenis, value=jenis))
	entry_jenis.pack(side=RIGHT,fill=X,pady=10, padx=10,expand=True)
	
	frame_pengirim = Frame(listbox_detailWindows)
	frame_pengirim.pack(fill=X)
	lbl_pengirim = Label(frame_pengirim, text="Pengirim", width=11)
	lbl_pengirim.pack(side=LEFT)
	entry_pengirim=Entry(frame_pengirim,textvariable=StringVar(frame_pengirim, value=pengirim))
	entry_pengirim.pack(side=RIGHT,fill=X,pady=10, padx=10,expand=True)
	
	frame_isi = Frame(listbox_detailWindows)
	frame_isi.pack(fill=X)
	lbl_isi = Label(frame_isi, text="Isi", width=11)
	lbl_isi.pack(side=LEFT)
	text_isi=Text(frame_isi)
	text_isi.insert(END, isi)
	text_isi.pack(side=RIGHT,fill=X,pady=10, padx=10,expand=True)
	
def check_past(BaseWindows):		
	try:
		rdata = s.recv(2048)
		if not rdata:
			BaseWindows.after_cancel(callback)
		elif rdata:
			#daftar_user.append(rdata)
			datas=rdata.split("\n")
			Frame=BaseWindows.winfo_children()
			widgets = Frame[2].winfo_children()
			for data in datas:
				if not data:
					continue
				elif str(data)=="SUKSES 100":
					continue
				else:
				#	widgets[1].config(state=NORMAL)
					widgets[1].insert(END,str(data))   
				#	widgets[1].config(state=DISABLED)
			callback=BaseWindows.after(1000,check_past(BaseWindows))
	except:
		callback=0
		
		#Frame=BaseWindows.winfo_children()
		#widgets = Frame[2].winfo_children()
		#scrollbar = Scrollbar(widgets[1])
		#idgets[1].config(yscrollcommand=scrollbar.set,height=23)
		#scrollbar.config(command=widgets[1].yview)
		#scrollbar.pack(side=RIGHT, fill=Y)
		print("Log Chat DIdapatkan")
def refresh(BaseWindows,indeks):
	if (indeks==0):
		s.sendall("check")
		indeks=indeks+1
		callback=BaseWindows.after(1000,refresh(BaseWindows,indeks))
	else:
		try:
			rdata = s.recv(2048)
			print(rdata)
			if not rdata:
				BaseWindows.after_cancel(callback)
			elif rdata:
			#daftar_user.append(rdata)
				datas=rdata.split("\n")
				Frame=BaseWindows.winfo_children()
				widgets = Frame[2].winfo_children()
				for data in datas:
					if not data:
						continue
					elif str(data)=="SUKSES 100":
						continue
					else:
						widgets[1].config(state=NORMAL)
						widgets[1].insert(END,str(data)+"\n")   
						widgets[1].config(state=DISABLED)
				callback=BaseWindows.after(1000,refresh(BaseWindows,indeks))
		except:
			callback=0
			print("BErhasil Diupdate")
def logout(BaseWindows):
	global user_login
	Frame_logout=BaseWindows.winfo_children()
	s.sendall("logout")
	terima=s.recv(4096)
	status_kode=terima.split()
	show_status_code(status_kode[1])
	if (str(status_kode[1])=="100"):
		user_login=""
		MenuLogin(BaseWindows)	
def register(BaseWindows):
	Frame_register=BaseWindows.winfo_children()
	widgets_register = Frame_register[2].winfo_children()
	username= str(widgets_register[1].get())
	widgets_register = Frame_register[3].winfo_children()
	password= str(widgets_register[1].get())
	widgets_register = Frame_register[4].winfo_children()
	verif_password= str(widgets_register[1].get())
	s.sendall("register "+username+" "+password+" "+verif_password)
	terima=s.recv(4096)
	status_kode=terima.split()
	show_status_code(status_kode[1])
def send(BaseWindows):
	#Frame_send=BaseWindows.winfo_children()
	#widgets_send = Frame_send[2].winfo_children()
	#index_username= map(int,widgets_send[1].curselection())
	#usernames=widgets_send[1].get(0,END)
	#username=usernames[index_username[0]]
	#widgets_send = Frame_send[3].winfo_children()
	#pesan= str(widgets_send[0].get())
	#s.sendall("send "+username+" "+pesan)
	#terima=s.recv(4096)
	Frame_send=BaseWindows.winfo_children()
	widgets_send=Frame_send[3].winfo_children()
	usert=str(widgets_send[1].get())
	widgets_send=Frame_send[4].winfo_children()
	pesan=str(widgets_send[1].get())
	s.sendall("send "+usert+" "+pesan)
	terima=s.recv(4096)
	status_kode=terima.split()
	show_status_code(status_kode[1])
def broadcast(BaseWindows):	
	Frame_send=BaseWindows.winfo_children()
	widgets_send = Frame_send[2].winfo_children()
	pesan= str(widgets_send[0].get())
	s.sendall("broadcast "+pesan)
	terima=s.recv(4096)
	status_kode=terima.split()
	show_status_code(status_kode[1])
def chatgroup(BaseWindows):	
	Frame_chatg=BaseWindows.winfo_children()
	widgets_chatg = Frame_chatg[2].winfo_children()
	nama_group= str(widgets_chatg[1].get())
	widgets_chatg = Frame_chatg[3].winfo_children()
	pesan= str(widgets_chatg[1].get())
	s.sendall("chatgroup "+nama_group+" "+pesan)
	terima=s.recv(4096)
	status_kode=terima.split()
	show_status_code(status_kode[1])
def joingroup(BaseWindows):	
	Frame_joing=BaseWindows.winfo_children()
	widgets_joing = Frame_joing[2].winfo_children()
	nama_group= str(widgets_joing[1].get())
	widgets_joing = Frame_joing[3].winfo_children()
	password_group= str(widgets_joing[1].get())
	s.sendall("joingroup "+nama_group+" "+password_group)
	terima=s.recv(4096)
	status_kode=terima.split()
	show_status_code(status_kode[1])			
def creategroup(BaseWindows):	
	Frame_createg=BaseWindows.winfo_children()
	widgets_createg = Frame_createg[2].winfo_children()
	nama_group= str(widgets_createg[1].get())
	widgets_createg = Frame_createg[3].winfo_children()
	password_group= str(widgets_createg[1].get())
	s.sendall("creategroup "+nama_group+" "+password_group)
	terima=s.recv(4096)
	status_kode=terima.split()
	show_status_code(status_kode[1])	
if __name__ == '__main__':
	BaseWindows = Tk()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5)
	connect_server()		
	MenuLogin(BaseWindows)
	#MenuJoin(BaseWindows)
	mainloop()
