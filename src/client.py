import socket
from rtsp_packet import rtspPacket

class Client():
    def __init__(self, args):
        self.ip = args.ip
        self.port = args.port
        self.timeout = args.timeout/1000
        self.valid_operations = ['setup', 'play', 'pause', 'tearDown']
        
        self.connected = False
        self.seq = 0
        pass
        
    def connect(self):
        self.rtsp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rtsp_s.connect((self.ip, self.port))
        self.rtsp_s.settimeout(self.timeout)
        self.connected = True
    
    def disconnect(self):
        self.rtsp_s.close()

    def send_request(self, operation):
        operation = operation.upper()
        print("%s Request Sending..." % operation)
        packet = rtspPacket(
            packet_type=operation,
            seqNum=self.seq,
            port=self.port,
            sessionId=1234
        ).buildRequest()

        if not self.connected:
            raise Exception('Connection not found! Please connect to server first.')
        
        print(f"Sending request: {repr(packet.decode())}")
        self.rtsp_s.send(packet)
        self.seq += 1
        return True


    # For Debug
    def shell(self):
        print("Connecting to RTSP server at %s:%s" % (self.ip, self.port))
        self.connect()
        while True:
            operation_type = input("> ")
            if operation_type == "exit":
                self.disconnect()
                break
            elif operation_type not in self.valid_operations:
                print("Operation Not Permitted!!!")
                print("Try the following oprtations: " + ", ".join(list(self.valid_operations)))
                continue
            else:
                self.send_request(operation_type)
            print()
        

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', default='127.0.0.1', type=str, metavar='<IP>',
                    help='IP for target rtsp server')
    parser.add_argument('--port', default=7777, type=int, metavar='<port>',
                    help='port of target rtsp server')
    parser.add_argument('--operation', default='setup', type=str, choices=['setup', 'play', 'pause', 'tearDown'], metavar='<operation>',
                    help='operation_type to be sent')
    parser.add_argument('--timeout', default=1, type=int, metavar='<timeout>',
                    help='seconds to wait before timeout')
    # parser.add_argument('--interactive', default=False, type=bool,
    #                 help='Specified to activate interactive mode')
    parser.add_argument("--interactive", action="store_true", help='Activate interactive mode')

    args = parser.parse_args()
    
    client = Client(args)
    if args.interactive:
        client.shell()
    else:
        client.send_request(args.operation)
        client.disconnect()