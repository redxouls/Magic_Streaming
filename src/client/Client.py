import socket, time
from protocols.RTSP import RTSP
from protocols.RTP import RTP

from io import BytesIO
import numpy as np
from PIL import Image

import matplotlib.pyplot as plt
import cv2

class Client():
    DEFAULT_CHUNK_SIZE = 4096
    def __init__(self, args):
        self.ip = args.ip
        self.port = args.port
        self.rtp_port = args.rtp_port
        self.timeout = args.timeout
        self.rtp_timeout = args.rtp_timeout
        # self.valid_operations = ['setup', 'play', 'pause', 'teardown']
        self.operations = {
            "setup": self.setup,
            "play": self.play,
            "pause": self.pause,
            "teardown": self.tear_down,
        }
        self.connected = False
        self.seq = 0

        self.rtp_sockets = dict()
        
    def connect(self):
        self.rtsp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rtsp_s.connect((self.ip, self.port))
        self.rtsp_s.settimeout(self.timeout)
        self.connected = True
    
    def disconnect(self):
        self.rtsp_s.close()

    def setup(self):
        print("Setup")
        self.rtp_init('camera')
        # self.rtp_init('mic')

    def play(self):
        print("Play")
        while True:
            start = time.time()
            try:
                decode_img = self.rtp_get_frame('camera')
                cv2.imshow('frame', decode_img)
            except:
                print("Error frame drop")
            finally:
                time.sleep(0.1)
                print(1/(time.time() - start))
            # 若按下 q 鍵則離開迴圈
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def pause(self):
        print("pause")

    def tear_down(self):
        print("teardown")

    def send_request(self, operation, device):
        operation = operation.upper()
        print("%s Request Sending..." % operation)
        packet = RTSP(
            packet_type=operation,
            seq_num=self.seq,
            rtp_dst_port=self.rtp_port,
            session_id=0,
            file_path=device
        ).build_request()

        if not self.connected:
            raise Exception('Connection not found! Please connect to server first.')
        
        print(f"Sending request: {repr(packet.decode())}")
        self.rtsp_s.send(packet)
        self.seq += 1
        return True

    def handle_receive(self):
        try:    
            request_raw = self.rtsp_s.recv(4096)
            request = request_raw.decode()
            print(f"Received from server: {repr(request)}")
            if request == "":
                self.disconnect()
                return
        except socket.timeout:
            self.disconnect()
            return

    # For Debug
    def shell(self):
        print("Connecting to RTSP server at %s:%s" % (self.ip, self.port))
        self.connect()
        while True:
            operation_type = input("> ")
            if operation_type == "exit":
                self.disconnect()
                break
            elif operation_type not in self.operations:
                print("Operation Not Permitted!!!")
                print("Try the following oprtations: " + ", ".join(list(self.valid_operations)))
                continue
            else:
                start = time.time()
                self.send_request(operation_type, 'camera')
                self.operations[operation_type]()
                self.handle_receive()
                print((time.time() - start))                
            print()

    
    def rtp_init(self, device):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = self.rtp_port + len(self.rtp_sockets)
        s.bind(("127.0.0.1", port))
        s.settimeout(self.rtp_timeout / 1000.)
        self.rtp_sockets[device] = (s, port)

        
    def rtp_get_frame(self, device):
        rtp_socket, _ = self.rtp_sockets[device]

        recv = bytes()
        print('Waiting RTP packet...')
        if device == 'camera':
            eof = b'\xff\xd9'
        elif device == 'mic':
            eof = b'Sound End'
        
        while True:
            try:
                recv += rtp_socket.recv(self.DEFAULT_CHUNK_SIZE)
                if recv.endswith(eof):
                    break
            except socket.timeout:
                continue
        print(f"Packet Received!")
        received_packet = RTP.receive(recv)
        img_raw = received_packet.payload
        io_buf = BytesIO(img_raw)
        decode_img = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), 1)
        if (device == 'mic'):
            print(len(recv))
        return decode_img
        

if __name__ == "__main__":
    import argparse
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
    
    client = Client(args)
    if args.interactive:
        client.shell()
    else:
        client.connect()
        client.send_request(args.operation)
        client.disconnect()