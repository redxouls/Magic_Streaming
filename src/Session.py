from rtsp_packet import rtspPacket


class Session:
    def __init__(self, client, ip):
        self.ip = ip
        self.client = client
        self.mes = None
        self.operations = {
            "setup": self.handle_setup,
            "play": self.handle_play,
            "pause": self.handle_pause,
            "tearDown": self.handle_tearDown,
        }

    def handle_setup(self):
        print("Setup Request Sending...")

    def handle_play(self):
        print("Play Request Sending...")

    def handle_pause(self):
        print("Pause Request Sending...")

    def handle_tearDown(self):
        print("tearDown Request Sending...")

    def handle_error(self):
        print("Operation Not Permitted!!!")
        print(
            "Try the following oprtations: " + ", ".join(list(self.operations.keys()))
        )

    def handle_receive(self):
        self.mes = self.client.recv(4096)
        print(f"Received from client: {repr(self.mes.decode())}")
        if self.mes.decode() == "":
            return False

        self.rtsp_packet = rtspPacket.getRequest(self.mes)
        self.operations[self.rtsp_packet.packet_type.lower()]()

        return True, self.ip

    def close_connection(self):
        self.client.close()
