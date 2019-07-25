import socket
import threading
from protocol import PacketHandler

# TODO: rewrite so threads are named and identifiable.
# TODO: make server more error robust (e.g. catch errors and report them but don't fail)


class Server(PacketHandler):
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
        # TODO: Merge the following two maps at some point.
        self.clients = {}
        self.cfg_map = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))

    def _register_client(self, client, address):
        self.clients[address] = client

    # TODO: refactor this, slightly dirty implementation, might be best to roll it later
    def _register_client_cfg(self, key, val, address):
        if address not in self.cfg_map:
            self.cfg_map[address] = {}
        self.cfg_map[address][key] = val

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

    def _client_loop(self, client, address):
        while True:
            try:
                packet = client.recv(self.buffer_size)
                if packet:
                    self.handle_packet(packet, address)
                else:
                    raise socket.error("Client disconnected.")
            except (socket.timeout, socket.error):
                print("{} dropped.".format(address))
                client.close()
                return False

    def handle_message(self, data, address):
        formatted = "{}: {}".format(self.cfg_map[address]["preferred_nickname"], data["body"])
        print(formatted.strip())
        self._broadcast(formatted.encode(), [address])

    # TODO: this method of handling is probably a security concern, there should be specific
    # configuration messages (to edit specific keys) we should implement this later.
    def handle_config(self, data, address):
        self.cfg_map[address] = data

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
