import socket
import time

ADDRESS = ('localhost', 413)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
	s.connect(ADDRESS)
	while True:
		try:
			data = None
			data = s.recv(1024).decode()
			if data != None:
				print(data)
		except KeyboardInterrupt:
			# needs threading, right now is blocked until new client connects -R
			s.close()
			
main()