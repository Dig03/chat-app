import socket
import threading

ADDRESS = ('localhost', 413)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def message_listener():
    while True:
        data = s.recv(1024)
        if data:
            print(data.decode())

def main():
    s.connect(ADDRESS)
    threading.Thread(target=message_listener).start()
    while True:
        try:
            s.send(input().encode())
        except KeyboardInterrupt:
            # needs threading, right now is blocked until new client connects -R
            s.close()


main()