# Simple protocol system to deal with network events in an extensible way.

# A lot of this is very draft-y so feel free to change.

import json


class PacketHandler:
    """
    Adds functions for event handling incoming packets.
    """

    def handle_message(self, data):
        """
        Handle a message packet.
        :param data: Message data.
        :return: Nothing.
        """
        raise NotImplementedError("Please implement this method.")

    def handle_command(self, data):
        """
        Handle a command packet.
        :param data: Command data.
        :return: Nothing.
        """
        raise NotImplementedError("Please implement this method.")

    def handle_

    def handle_packet(self, packet):
        """
        Our "Packets" could have a form like:
        {
            "kind": "message",
            "data": { ... }
        }
        Where the data key contains an arbitrary information relevant to the type.
        For example a message packet may have data fields like time sent, or the message body, and a command packet
        would contain information like the command to execute and parameters.

        TODO: to save data we could make the "types" single digit byte objects or something and then create a mapping
        like 0 - message, 1 - command etc, but we can implement that later.

        TODO: define message "kinds" as constants for easy changing.

        TODO: could take the bytes object and convert it using json in the protocol to make all json-dealing occur
        within this handler (for proper segregation).

        :param packet: The packet to handle.
        :return: Nothing. Calls relevant function to handle the appropriate packet type.
        """
        funcs = {
            "message": self.handle_message,
            "command": self.handle_command
        }
        try:
            funcs[packet["kind"]](packet["data"])
        except KeyError:
            raise KeyError("\"{}\" is not a valid kind for a packet.".format(packet["kind"]))


class PacketBuilder:
    """
    Adds functions for constructing valid packets which can be interpreted in our client-server model.
    """

    @staticmethod
    def build_message(body):
        """
        Build a message packet.
        :param body: Body of the message.
        :return: Bytes object ready to send through socket interface.
        """
        return json.dumps({"type": "message", "data": {"body": body}}).encode()
