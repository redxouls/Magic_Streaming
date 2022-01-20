from client.Client import Client
from object_detect import object_detection
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', default='127.0.0.1', type=str, metavar='<IP>',
                    help='IP for target rtsp server')
    parser.add_argument('--port', default=7777, type=int, metavar='<port>',
                    help='port of target rtsp server')
    parser.add_argument('--rtp-port', default=20202, type=int, metavar='<rtp-port>',
                    help='port to listen rtp stream')
    parser.add_argument('--operation', default='setup', type=str, choices=['setup', 'play', 'pause', 'teardown'], metavar='<operation>',
                    help='operation_type to be sent')
    parser.add_argument('--timeout', default=5, type=int, metavar='<timeout>',
                    help='seconds to wait before timeout rtsp session')
    parser.add_argument('--rtp-timeout', default=5, type=int, metavar='<rtp-timeout>',
                    help='seconds to wait before timeout rtp session')
    parser.add_argument("--interactive", action="store_true", help='Activate interactive mode')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    print(args)
    detector = object_detection("yolov5s.pt")
    client = Client(args, detector)
    if args.interactive:
        client.shell()
    else:
        client.connect()
        client.send_request(args.operation)
        client.disconnect()