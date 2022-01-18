import socket, threading
from rtsp_packet import rtspPacket
from Session import Session
import uuid


class Server:
    def __init__(self, args):
        self.ip = args.ip
        self.port = args.port
        self.verbose = args.verbose
        self.timeout = args.timeout / 1000
        self.sessions = {}

    def server_init(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip, self.port))
        self.s.listen(5)
        self.s.setblocking(False)
        print("RTSP server listening at %s:%s" % (self.ip, self.port))

    def accept_connection(self):
        try:
            client, client_ip = self.s.accept()
            client.settimeout(self.timeout / 1000)
            print(client_ip, client_ip)
            self.sessions[str(uuid.uuid4())] = Session(client=client, ip=client_ip)
        except:
            pass

    def on_client(self):
        toDel = []
        for session, id in zip(self.sessions.values(), self.sessions.keys()):
            try:
                alive = session.handle_receive()
                if not alive:
                    print("close {}".format(id))
                    session.close_connection()
                    toDel.append(id)
            except socket.timeout:
                pass
        for id in toDel:
            del self.sessions[id]

    def main(self):
        self.server_init()
        while True:
            self.accept_connection()
            self.on_client()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip", default="127.0.0.1", type=str, metavar="<IP>", help="IP for rtsp server"
    )
    parser.add_argument(
        "--port",
        default=7777,
        type=int,
        metavar="<port>",
        help="port for rtsp server to listen",
    )
    parser.add_argument(
        "--timeout",
        default="1",
        type=int,
        metavar="<timeout>",
        help="wait time before diconnection",
    )
    parser.add_argument("--verbose", action="store_true", help="Show debug messages")
    args = parser.parse_args()

    server = Server(args)
    server.main()
