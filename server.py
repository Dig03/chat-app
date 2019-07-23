# Simple broadcast server.

import socket

CFG = ('', 413)
MAX_CONNECTIONS = 100

iface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
iface.bind(CFG)
iface.listen(MAX_CONNECTIONS)
print("Running.")

clients = []

def main():
    try:
        while True:
            client_iface, addr = iface.accept()
            print("Accepted {}.".format(addr))
            clients.append(client_iface)
            message_clients(clients, "{} joined!".format(addr))
    except KeyboardInterrupt:
        # needs threading, right now is blocked until new client connects -R
        iface.close()


def message_clients(clients, message):
    for client in clients:
        client.send(message.encode())


if __name__ == '__main__':
    main()
