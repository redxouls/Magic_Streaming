import socket, uuid
from .Session import Session


class Server:
    def __init__(self, args):
        self.ip = args.ip
        self.port = args.port
        self.verbose = args.verbose
        self.timeout = args.timeout
        self.sessions = {}

    def server_init(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip, self.port))
        self.s.listen(0)
        print("RTSP server listening at %s:%s" % (self.ip, self.port))

    def accept_connection(self):
        client, client_addr = self.s.accept()
        client.settimeout(self.timeout)
        print(client_addr)
        incoming_session_id = str(uuid.uuid4())
        incoming_session = Session(
            client=client, client_addr=client_addr, rtsp_session_id=incoming_session_id
        )
        incoming_session.listen()
        self.sessions[incoming_session_id] = incoming_session

    def clean_timeout(self):
        to_del = [
            session_id
            for session_id, session in self.sessions.items()
            if session.client.fileno() == -1
        ]
        to_del_num = len(to_del)
        for session_id in to_del:
            del self.sessions[session_id]

        print(
            "Toal session: %s, Release session# = %d" % (len(self.sessions), to_del_num)
        )

    def main(self):
        self.server_init()
        while True:
            self.clean_timeout()
            self.accept_connection()


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
        default="100000",
        type=int,
        metavar="<timeout(second)>",
        help="wait time before diconnection (second)",
    )
    parser.add_argument("--verbose", action="store_true", help="Show debug messages")
    args = parser.parse_args()

    server = Server(args)
    server.main()
