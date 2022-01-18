import socket, threading


class Server():
    def __init__(self, args):
        self.ip = args.ip
        self.port = args.port
        self.verbose = args.verbose
        self.timeout = args.timeout / 1000
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
        print("Try the following oprtations: " + ", ".join(list(self.operations.keys())))

    def server_init(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip, self.port))
        self.s.listen(1)
        print("RTSP server listening at %s:%s" % (self.ip, self.port))

    def accept_connection(self):
        self.client, self.client_ip = self.s.accept()
        self.client.settimeout(self.timeout / 1000)
        print(self.client_ip, self.client_ip)
    
    def handle_receive(self):
        received = None
        while True:
            try:
                received = self.client.recv(4096)
                break
            except socket.timeout:
                continue
        print(f"Received from client: {repr(received.decode())}")
        return received
    
    def close_connection(self):
        self.client.close()

    def on_client(self):
        while True:
            received = self.handle_receive()
            if len(received) == 0:
                self.close_connection()
                break

    def main(self):
        self.server_init()
        while True:
            self.accept_connection()
            self.on_client()
            

            


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', default='127.0.0.1', type=str, metavar='<IP>',
                    help='IP for rtsp server')
    parser.add_argument('--port', default=7777, type=int, metavar='<port>',
                    help='port for rtsp server to listen')
    parser.add_argument('--timeout', default='1', type=int, metavar='<timeout>',
                    help='wait time before diconnection')
    parser.add_argument("--verbose", action="store_true", help='Show debug messages')
    args = parser.parse_args()
    
    server = Server(args)
    server.main()