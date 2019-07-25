import socket
import threading
import json


class Server:
    """
    Relatively simple threaded chat server.
    """

    def __init__(self, host, port, max_connections=100, buffer_size=1024, timeout=60):
        """
        Construct a Server.

        :param host: interface IP to bind to
        :param port: port to bind to
        :param max_connections: maximum number of concurrent connections
        :param buffer_size: maximum buffer for a single received message
        :param timeout: time to wait (in seconds) for an operation on a client to complete
        """
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.buffer_size = buffer_size
        self.timeout = timeout
        self.clients = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))

    def _register_client(self, client, address):
        self.clients[address] = client

    def _broadcast(self, message, exclude=None):
        """
        Transmit a message to all clients except those in exclude.

        :param message: bytes object to broadcast.
        :param exclude: list of addresses to not broadcast to.
        """
        if exclude is None:
            exclude = []
        for address in self.clients:
            if address not in exclude:
                self.clients[address].send(message)

    # TODO: split code off into packet handlers so functions remain individually small

    def _client_loop(self, client, address):
        client_cfg = {}
        while True:
            try:
                data = json.loads(client.recv(self.buffer_size))
                if data:
                    if data["type"] == "message":
                        formatted = "{}: {}".format(client_cfg[client]["preferred_nickname"], data["payload"])
                        print(formatted.strip())
                        self._broadcast(formatted.encode(), [address])
                    elif data["type"] == "client_cfg":
                        client_cfg[client] = data["payload"]

                    else:
                        print("Ignored invalid packet from {}, type {}.".format(address, data["type"]))
                else:
                    raise socket.error("Client disconnected.")
            except (socket.timeout, socket.error):
                print("{} dropped.".format(address))
                client.close()
                return False

    def listen(self):
        self.sock.listen(self.max_connections)
        print("Listening on {}:{}.".format(self.host, self.port))
        while True:
            client, address = self.sock.accept()
            print("Received connection from {}.".format(address))
            client.settimeout(self.timeout)
            self._register_client(client, address)
            threading.Thread(target=self._client_loop, args=(client, address)).start()


if __name__ == '__main__':
    Server('', 413).listen()
