import json
import socket
import threading
import os
from protocol import PacketBuilder

ADDRESS = ('localhost', 413)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Client(PacketBuilder):

    def __init__(self, host="localhost", port=413):
        self.host = host
        self.port = port

    # TODO: use JSON config instead? looks pretty good otherwise

    @staticmethod
    def gen_configs():
        try:
            os.makedirs("client")
            print("Directory /client/ created to store local configs")
        except FileExistsError:
            print("Directory /client/ already exists, continuing...")
        with open("client/config.cfg", "w+") as f:
            f.write("preferred_nickname=boring person")
            # more config options go here

    # TODO: rewrite this into dedicated protocol buiilder functions?
    @staticmethod
    def generate_packet(ptype, payload=None):
        p = {"kind": ptype, "data": payload}
        return json.dumps(p).encode()

    def startup(self):
        if os.path.isfile('client/config.cfg'):
            with open("client/config.cfg", "r") as f:
                f.seek(0)
                cfgs = {}
                cfgs["preferred_nickname"] = f.readlines()[0].split("=")[1]
        else:
            print("Configs not present, generating now...")
            self.gen_configs()
            self.startup()
        s.connect(ADDRESS)
        s.send(self.build_config(cfgs))
        print("Connection successful to {}".format(s.getsockname()))
        threading.Thread(target=self.message_listener).start()

    @staticmethod
    def message_listener():
        while True:
            data = s.recv(1024).decode()
            if data:
                print(data)

    def main(self):
        self.startup()
        while True:
            try:
                s.send(self.build_message(input()))
            except KeyboardInterrupt:
                # needs threading, right now is blocked until new client connects -R
                s.close()


Client(input("IP to connect to: ")).main()
