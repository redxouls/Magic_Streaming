import socket, time, threading
import pyaudio

from io import BytesIO
import numpy as np
from PIL import Image
import cv2

from protocols.RTSP import RTSP
from protocols.RTP import RTP

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
TIME = 0.023219954648526078
CHUNK = 1024


class Client:
    DEFAULT_CHUNK_SIZE = 4096

    def __init__(self, args, detector):
        self.ip = args.ip
        self.port = args.port
        self.rtp_port = args.rtp_port
        self.timeout = args.timeout
        self.rtp_timeout = args.rtp_timeout

        self.operations = {
            "setup": self.setup,
            "play": self.play,
            "pause": self.pause,
            "teardown": self.tear_down,
        }
        self.connected = False
        self.seq = 0

        # NOTE: is_pause and is_teardown
        self.is_streaming = False

        self.rtp_sockets = dict()
        self.threads = dict()
        self.detector = detector
        self.results = []
        self.decode_img = None
        self.img_buffer = []
        self.img_timestamp = []

    def connect(self):
        self.rtsp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rtsp_s.connect((self.ip, self.port))
        self.rtsp_s.settimeout(self.timeout)
        self.connected = True

    def disconnect(self):
        self.rtsp_s.close()

    def setup(self):
        print("Setup")
        self.rtp_init("camera")
        self.send_request("setup", "camera")
        self.handle_receive()

        self.rtp_init("mic")
        self.send_request("setup", "mic")
        self.handle_receive()

    def play(self):
        print("Play")
        self.send_request("play", "mic")
        self.handle_receive()

        self.threads["mic"] = threading.Thread(target=self.stream_audio)
        self.threads["mic"].start()

        self.send_request("play", "camera")
        self.handle_receive()

        self.threads["camera"] = threading.Thread(target=self.stream_video)
        self.threads["camera"].start()

    def stream_audio(self):
        self.is_streaming = True
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            output=True,
            frames_per_buffer=CHUNK,
        )
        eof = b"Sound End"
        try:
            while self.is_streaming:
                data, timestamp = self.rtp_get_raw("mic")
                data = data[: -len(eof)]
                stream.write(data)
                # time.sleep(0.007)
        except KeyboardInterrupt:
            return
        except:
            stream.close()
            audio.terminate()

    def stream_video(self):
        self.is_streaming = True
        counts = 0
        self.results = []
        while self.is_streaming:
            start = time.time()
            try:
                img_raw, timestamp = self.rtp_get_raw("camera")
                self.img_buffer.append(img_raw)
                self.img_timestamp.append(timestamp)
                if len(self.img_buffer) >= 10:
                    img_raw = self.img_buffer.pop(0)
                    io_buf = BytesIO(img_raw)
                    decode_img = cv2.imdecode(
                        np.frombuffer(io_buf.getbuffer(), np.uint8), 1
                    )
                    #  TO DO HERE
                    if counts % 10 == 0:
                        self.results = self.detector.bounding_box(decode_img)

                    emphasize = []
                    for r in self.results:
                        emphasize.append(
                            decode_img[r[0][1] : r[1][1], r[0][0] : r[1][0], :]
                        )

                    decode_img = cv2.blur(decode_img, (30, 30))

                    for i, img in enumerate(emphasize):
                        decode_img[
                            self.results[i][0][1] : self.results[i][1][1],
                            self.results[i][0][0] : self.results[i][1][0],
                            :,
                        ] = img
                    decode_img = cv2.cvtColor(decode_img, cv2.COLOR_BGR2RGB)
                    self.decode_img = Image.fromarray(decode_img)

            except Exception as e:
                print("Error frame drop")
                print(e)
            finally:
                print(counts, time.time() - start)
                if counts % 10 != 0:
                    time.sleep(0.05)
                counts += 1

    def pause(self):
        print("pause")
        self.is_streaming = False
        self.send_request("pause", "mic")
        self.handle_receive()
        time.sleep(0.05)
        self.send_request("pause", "camera")
        self.handle_receive()

    def tear_down(self):
        print("teardown")
        self.is_streaming = False
        self.send_request("pause", "mic")
        self.handle_receive()
        time.sleep(0.05)
        self.send_request("pause", "camera")
        self.handle_receive()
        self.rtp_sockets["mic"][0].close()
        self.rtp_sockets["camera"][0].close()

        self.rtp_sockets = {}
        self.threads = {}
        self.decode_img = None

    def send_request(self, operation, device):
        operation = operation.upper()
        print("%s Request Sending..." % operation)
        packet = RTSP(
            packet_type=operation,
            seq_num=self.seq,
            rtp_dst_port=self.rtp_sockets[device][1],
            session_id=0,
            file_path=device,
        ).build_request()

        if not self.connected:
            raise Exception("Connection not found! Please connect to server first.")

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
                print(
                    "Try the following oprtations: "
                    + ", ".join(list(self.valid_operations))
                )
                continue
            else:
                start = time.time()

                self.operations[operation_type]()

                print((time.time() - start))
            print()

    def rtp_init(self, device):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = self.rtp_port + len(self.rtp_sockets)
        s.bind(("0.0.0.0", port))
        s.settimeout(self.rtp_timeout / 1000.0)
        self.rtp_sockets[device] = (s, port)

    def rtp_get_raw(self, device):
        rtp_socket, _ = self.rtp_sockets[device]

        recv = bytes()
        if device == "camera":
            eof = b"\xff\xd9"
        elif device == "mic":
            eof = b"Sound End"

        while True:
            try:
                recv += rtp_socket.recv(self.DEFAULT_CHUNK_SIZE)
                if recv.endswith(eof):
                    break
            except socket.timeout:
                continue
        received_packet = RTP.receive(recv)
        raw = received_packet.payload
        timestamp = received_packet.timestamp

        # print("device: {}".format(device), timestamp/100)
        return raw, timestamp


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip",
        default="127.0.0.1",
        type=str,
        metavar="<IP>",
        help="IP for target rtsp server",
    )
    parser.add_argument(
        "--port",
        default=7777,
        type=int,
        metavar="<port>",
        help="port of target rtsp server",
    )
    parser.add_argument(
        "--rtp-port",
        default=20202,
        type=int,
        metavar="<rtp-port>",
        help="port to listen rtp stream",
    )
    parser.add_argument(
        "--operation",
        default="setup",
        type=str,
        choices=["setup", "play", "pause", "teardown"],
        metavar="<operation>",
        help="operation_type to be sent",
    )
    parser.add_argument(
        "--timeout",
        default=5,
        type=int,
        metavar="<timeout>",
        help="seconds to wait before timeout rtsp session",
    )
    parser.add_argument(
        "--rtp-timeout",
        default=5,
        type=int,
        metavar="<rtp-timeout>",
        help="seconds to wait before timeout rtp session",
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Activate interactive mode"
    )

    args = parser.parse_args()

    client = Client(args)
    if args.interactive:
        client.shell()
    else:
        client.connect()
        client.send_request(args.operation)
        client.disconnect()
