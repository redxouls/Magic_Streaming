import argparse
from server.Server import Server

def get_args():
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
        default="10000",
        type=int,
        metavar="<timeout(second)>",
        help="wait time before diconnection (second)",
    )
    parser.add_argument("--verbose", action="store_true", help="Show debug messages")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    server = Server(args)
    server.main()