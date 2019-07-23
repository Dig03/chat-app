import socket
import threading


class Server:
    """
    Relatively simple threaded chat server.
    """

    """
    Arguments:
        host: interface IP for server to bind to
        port: port to bind to
        max_connections: maximum number of possible accepted connections
        bufsize: maximum buffer for a single received message
        timeout: time to wait (in seconds) for an operation on a client to complete
    """
    def __init__(self, host, port, max_connections = 100, bufsize = 1024, timeout = 60):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.bufsize = bufsize
        self.timeout = timeout
        self.clients = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))

    def _register_client(self, client, address):
        self.clients[address] = client

    """
    Transmit a message to all clients except those in exclude.
    
    Arguments:
        message: bytes object to broadcast.
        exclude: a list of addresses to not broadcast to.
    """
    def _broadcast(self, message, exclude=None):
        if exclude is None:
            exclude = []
        for address in self.clients:
            if address not in exclude:
                self.clients[address].send(message + '\n')

    def listen(self):
        self.sock.listen(self.max_connections)
        print("Listening on {}:{}.".format(self.host, self.port))
        while True:
            client, address = self.sock.accept()
            print("Received connection from {}.".format(address))
            client.settimeout(self.timeout)
            self._register_client(client, address)
            threading.Thread(target=self.client_loop, args=(client, address)).start()

    def client_loop(self, client, address):
        while True:
            try:
                data = client.recv(self.bufsize)
                if data:
                    formatted = "{}: {}".format(address, data)
                    print(formatted)
                    self._broadcast(formatted.encode(), [address])
                else:
                    raise socket.error("Client disconnected.")
            except (socket.timeout, socket.error):
                print("{} dropped.".format(address))
                client.close()
                return False


if __name__ == '__main__':
    Server('', 413).listen()
