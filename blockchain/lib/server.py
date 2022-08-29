#!usr/bin/python

#block_server.py

import socket

s = socket.socket()

host = socket.gethostname()
port = 12345

s.bind((host,port))
s.listen(5)

while True:
    conn, addr = s.accept()		# accept the connection

    conn.settimeout(2)
    #data = conn.recv(1024)	
    while 1:			        # till data is coming
        try:
            data = conn.recv(1024)
            
        except socket.timeout:
            print("here")
            continue
        print(data)
    print("All Data Received")	# Will execute when all data is received
    conn.close()
    break