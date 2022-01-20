import re

class RTSP:
    RTSP_VERSION = 'RTSP/1.0'

    def __init__(self, packet_type: str, session_id: int, seq_num: int, file_path=None, rtp_dst_port=None):
        self.packet_type = packet_type
        self.session_id = session_id
        self.seq_num = seq_num
        self.file_path = file_path
        self.rtp_dst_port = rtp_dst_port

    @classmethod
    def get_response(cls, response: bytes):
        response = response.decode()
        match = re.match(
            r"(?P<rtsp_version>RTSP/\d+.\d+)\r?\n"
            r"Seq: (?P<sequence_number>\d+)\r?\n"
            r"Session: (?P<session_id>\d+)\r?\n",
            response
        )
        if match is None:
            raise Exception(f'Fail to parse: \n{response}')
        res = match.groupdict()

        return cls(
            packet_type='RESPONSE',
            session_id=int(res['session_id']),
            seq_num=int(res['sequence_number'])
        )

    @classmethod
    def get_request(cls, request: bytes):
        request = request.decode()
        match = re.match(
            r"(?P<packet_type>\w+) rtsp://(?P<video_file_path>\S+) (?P<rtsp_version>RTSP/\d+.\d+)\r?\n"
            r"Seq: (?P<sequence_number>\d+)\r?\n"
            r"(Range: (?P<play_range>\w+=\d+-\d+\r?\n))?"
            r"(Transport: RTP/UDP;client_port=(?P<rtp_dst_port>\d+).*\r?\n)?"  # in case of SETUP request
            r"(Session: (?P<session_id>\d+)\r?\n)?",
            request
        )

        if match is None:
            raise Exception(f'Fail to parse: \n{request}')
        req = match.groupdict()
        if req['packet_type']=='SETUP' and req['session_id']==None:
            req['session_id'] = -1
        
        return cls(
            packet_type=req['packet_type'],
            session_id=int(req['session_id']),
            seq_num=int(req['sequence_number']),
            file_path=req['video_file_path'],
            rtp_dst_port=req['rtp_dst_port']
        )

    def build_response(self) -> bytes:
        if self.packet_type!='RESPONSE':
            raise Exception('Wrong type, should be RESPONSE')
        response = '\r\n'.join((
            f"{self.RTSP_VERSION}",
            f"Seq: {self.seq_num}",
            f"Session: {self.session_id}",
        )) + '\r\n'
        return response.encode()

    def build_request(self) -> bytes:
        if any((attr is None for attr in (self.packet_type, self.seq_num, self.session_id))):
            raise Exception('Missing attribute')
        if self.packet_type=='RESPONSE':
            raise Exception('Invalid request packet_type: Response')
        request_lines = [
            f"{self.packet_type} rtsp://{self.file_path} {self.RTSP_VERSION}",
            f"Seq: {self.seq_num}",
        ]
        if self.packet_type=='SETUP':
            if self.rtp_dst_port is None:
                raise Exception('Missing RTP destination port')
            request_lines.append(f"Transport: RTP/UDP;client_port={self.rtp_dst_port}")
        else:
            request_lines.append(f"Session: {self.session_id}")
        request = '\r\n'.join(request_lines) + '\r\n'
        return request.encode()
