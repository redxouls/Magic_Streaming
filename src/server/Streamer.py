import socket, time, threading, sys
from protocols.RTP import RTP
from .Camera import Camera
from .Mic import Mic

class Streamer:
    DEFAULT_CHUNK_SIZE = 4096
    class MEDIA_TYPE:
        STRING = 0

    def __init__(self, client_ip):
        # , client_port,  file_path
        self.client_ip = client_ip
        self.rtp_sockets = dict()
        self.devices = dict()
        self.threads = dict()
        self.available_devices = {
            "camera": Camera,
            "mic": Mic
        }        
        
    def start_stream(self, device):
        print("Starting streaming %s" % device)
        self.threads[device] = threading.Thread(target=self.stream, args=(device,))
        self.threads[device].start()
        print("Daemon %s" % device)

    def stream(self, device):
        print("Start Streaming video to target client")        
        while True:
            # frame = self._video_stream.get_next_frame()
            # frame_number = self._video_stream.current_frame_number
            
            frame = self.devices[device].get_frame()
            if frame:
                rtp_packet = RTP(
                    payload_type=self.MEDIA_TYPE.STRING,
                    seq_num=0,
                    timestamp=int(time.time()),
                    payload=frame
                )
                # print(f"Sending packet #{frame_number}")
                # print('Packet header:')
                # rtp_packet.print_header()
                packet = rtp_packet.get_packet()
                self.send_rtp_packet(device, packet)
                if device == 'mic':
                    time.sleep(0.0095)
                else:
                    time.sleep(0.1)
    def send_rtp_packet(self, device, packet):
        rtp_socket, client_port = self.rtp_sockets[device]
        print(device, client_port)
        # if device == 'mic':
        #     return
        #     print(device, "sending", packet)
        to_send = packet[:]
        while to_send:
            try:
                rtp_socket.sendto(to_send[:self.DEFAULT_CHUNK_SIZE], (self.client_ip, client_port))
                time.sleep(0.0035)
            except socket.error as e:
                print(f"failed to send rtp packet: {e}")
                return
            to_send = to_send[self.DEFAULT_CHUNK_SIZE:]
    
    def add_device(self, port, device):
        if device not in self.available_devices:
            return
        self.devices[device] = self.available_devices[device]()
        print(self.devices)
        print("Add device: %s" % device)
        port = int(port)
        self.rtp_sockets[device] = (socket.socket(socket.AF_INET, socket.SOCK_DGRAM), port)
        print("Target: %s:%d" % (self.client_ip, port))

        

if __name__  == "__main__":
    video_streamer = VideoStreamer("video.mp4")