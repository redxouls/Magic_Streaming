import re
class rtspPacket:
    RTSP_VERSION = 'RTSP/1.0'

    def __init__(self, type: str, sessionId: int, seqNum: int, media=None, filePath=None, port=None):
        self.type = type
        self.sessionId = sessionId
        self.seqNum = seqNum
        self.media = media
        self.filePath = filePath
        self.port = port

    @classmethod
    def getResponse(cls, response: bytes):
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
            type='RESPONSE',
            sessionId=int(res['session_id']),
            seqNum=int(res['sequence_number'])
        )

    @classmethod
    def getRequest(cls, request: bytes):
        request = request.decode()
        match = re.match(
            r"(?P<request_type>\w+) rtsp://(?P<video_file_path>\S+) (?P<rtsp_version>RTSP/\d+.\d+)\r?\n"
            r"Seq: (?P<sequence_number>\d+)\r?\n"
            r"(Range: (?P<play_range>\w+=\d+-\d+\r?\n))?"
            r"(Transport: RTP/UDP;client_port=(?P<dst_port>\d+).*\r?\n)?"  # in case of SETUP request
            r"(Session: (?P<session_id>\d+)\r?\n)?",
            request
        )

        if match is None:
            raise Exception(f'Fail to parse: \n{request}')
        req = match.groupdict()
        if req['request_type']=='SETUP' and req['session_id']==None:
            req['session_id'] = -1
        
        return cls(
            type=req['request_type'],
            sessionId=int(req['session_id']),
            seqNum=int(req['sequence_number']),
            filePath=req['video_file_path'],
            port=req['dst_port']
        )

    def buildResponse(self) -> bytes:
        if self.type!='RESPONSE':
            raise Exception('Wrong type, should be RESPONSE')
        response = '\r\n'.join((
            f"{self.RTSP_VERSION}",
            f"Seq: {self.seqNum}",
            f"Session: {self.sessionId}",
        )) + '\r\n'
        return response.encode()

    def buildRequest(self) -> bytes:
        if any((attr is None for attr in (self.type, self.seqNum, self.sessionId))):
            raise Exception('Missing attribute')
        if self.type=='RESPONSE':
            raise Exception('Invalid request type: Response')
        request_lines = [
            f"{self.type} rtsp://{self.filePath} {self.RTSP_VERSION}",
            f"Seq: {self.seqNum}",
        ]
        if self.type=='SETUP':
            if self.port is None:
                raise Exception('Missing destination port')
            request_lines.append(f"Transport: RTP/UDP;client_port={self.port}")
        else:
            request_lines.append(f"Session: {self.sessionId}")
        request = '\r\n'.join(request_lines) + '\r\n'
        return request.encode()
