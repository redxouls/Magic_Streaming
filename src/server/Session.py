import socket, threading, time
from protocols.RTSP import RTSP
from .Streamer import Streamer


class Session:
    class STATE:
        INIT = 0
        PAUSED = 1
        PLAYING = 2
        FINISHED = 3
        TEARDOWN = 4

    def __init__(self, client, client_addr, rtsp_session_id):
        self.client = client
        self.client_addr = client_addr
        self.rtsp_session_id = rtsp_session_id
        self.rtsp = RTSP("RESPONSE", session_id=0, seq_num=0)

        self.operations = {
            "setup": self.on_setup,
            "play": self.on_play,
            "pause": self.on_pause,
            "teardown": self.on_tear_down,
        }
        self.streamer = Streamer(self.client_addr[0])
        # self.status = self.STATE.INIT

    def on_setup(self, rtsp_packet):
        # print("Handling setup request...")
        # if self.status != self.STATE.INIT:
        #     print("Exception: server is already setup")
        #     return False

        # self.status = self.STATE.PAUSED
        # print('State set to PAUSED')
        self.streamer.add_device(rtsp_packet.rtp_dst_port, rtsp_packet.file_path)
        print(rtsp_packet.file_path)

        return True

    def on_play(self, rtsp_packet):
        print("Handling play request Sending...")
        self.status = self.STATE.PLAYING
        self.streamer.start_stream(rtsp_packet.file_path)
        return True

    def on_pause(self, rtsp_packet):
        print("Pause Request Sending...")
        self.status = "pause"
        print(rtsp_packet.file_path)
        self.streamer.threads[rtsp_packet.file_path][1] = False
        return True

    def on_tear_down(self, rtsp_packet):
        print("tearDown Request Sending...")
        self.status = "teardown"
        self.streamer.threads[rtsp_packet.file_path][1] = False
        return True

    def on_error(self, rtsp_packet):
        print("Operation Not Permitted!!!")
        print(
            "Try the following oprtations: " + ", ".join(list(self.operations.keys()))
        )

    def handle_receive(self):
        while True:
            try:
                request_raw = self.client.recv(4096)
                request = request_raw.decode()
                if request == "":
                    self.close_connection()
                    return

                print(f"Received from client: {repr(request)}")
                request_rtsp_packet = self.rtsp.get_request(request_raw)
                if self.operations[request_rtsp_packet.packet_type.lower()](
                    request_rtsp_packet
                ):
                    self.send_response()

            except socket.timeout:
                self.close_connection()
                return

    def send_response(self):
        response = self.rtsp.build_response()
        self.client.send(response)
        self.rtsp.seq_num += 1
        print("Sent response to client.")

    def close_connection(self):
        print("Connection Closed rtsp_session_id: %s" % self.rtsp_session_id)
        self.client.close()

    def listen(self):
        print("Start listening request from %s" % self.rtsp_session_id)
        self.thread = threading.Thread(target=self.handle_receive)
        self.thread.start()
