import socket, time, threading, sys
from protocols.RTP import RTP
from .Camera import Camera

class Streamer:
    DEFAULT_CHUNK_SIZE = 4096
    class MEDIA_TYPE:
        STRING = 0

    def __init__(self, client_ip, client_port,  file_path):
        self.client_ip = client_ip
        self.client_port = int(client_port)
        self.file_path = file_path
        print(client_port)
        print("Video Streamer createrd for file: %s" % self.file_path)
        print("Target: %s:%d" % (self.client_ip, self.client_port))
        self.rtp_socket_init()
        self.camera = Camera()
        self.thread = None


    def rtp_socket_init(self):
        self.rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def start_stream(self):
        self.thread = threading.Thread(target=self.stream)
        self.thread.start()
    

    def stream(self):
        print("Start Streaming video to target client")        
        while True:
            # frame = self._video_stream.get_next_frame()
            # frame_number = self._video_stream.current_frame_number
            frame = self.camera.get_frame()
            rtp_packet = RTP(
                payload_type=self.MEDIA_TYPE.STRING,
                seq_num=0,
                timestamp=0,
                payload=frame
            )
            # print(f"Sending packet #{frame_number}")
            # print('Packet header:')
            # rtp_packet.print_header()
            packet = rtp_packet.get_packet()
            self.send_rtp_packet(packet)
            time.sleep(0.1)

    def send_rtp_packet(self, packet):
        to_send = packet[:]
        while to_send:
            try:
                self.rtp_socket.sendto(to_send[:self.DEFAULT_CHUNK_SIZE], (self.client_ip, self.client_port))
                time.sleep(0.0035)
            except socket.error as e:
                print(f"failed to send rtp packet: {e}")
                return
            to_send = to_send[self.DEFAULT_CHUNK_SIZE:]

if __name__  == "__main__":
    video_streamer = VideoStreamer("video.mp4")