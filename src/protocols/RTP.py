class RTP:
    HEADERSIZE = 12

    def __init__(
        self,
        payload_type: int,
        seq_num: int,
        timestamp: int,
        payload: bytes,
        padding: bool = False,
        Extension: bool = False,
        CSRC_count: int = 0x0,
        Marker: int = 0b0,
        SSRC: int = 0x00000000,
        CSRC: int = None,
        extension_bits: bytes = None,
    ):
        """RTP

        Args:
            payload_type (int): 7 bits. Ref: https://www.rfc-editor.org/rfc/rfc3551#page-32 .
            seq_num (int): 16 bits.
            timestamp (int): 32 bits.
            payload (bytes): Your payload
            padding (bool, optional): 1 bit. Whether to pad payload to 4*n bytes. Defaults to False.
            Extension (bool, optional): 1 bit. Defaults to False.
            CSRC_count (int, optional): 4 bits. Defaults to 0x0.
            Marker (int, optional): 1 bit Defaults to 0b0.
            SSRC (int, optional): 32 bits. Defaults to 0x00000000.
            CSRC (int, optional): 32 bits. Defaults to None.
            extension (bytes, optional): The first 32-bit word contains a profile-specific identifier (16 bits) and a length specifier (16 bits) that indicates the length of the extension in 32-bit units, excluding the 32 bits of the extension header. Defaults to None.
        """
        self.Version = 2
        self.P = int(padding)
        self.X = int(Extension)
        self.CC = CSRC_count
        self.M = Marker
        self.PT = payload_type
        self.seq_num = seq_num
        self.timestamp = timestamp
        self.SSRC = SSRC
        self.CSRC = CSRC
        self.extension_bits = extension_bits
        self.payload = payload

        header_bytes = []
        header_bytes.append(self.Version << 6 | self.P << 5 | self.X << 4 | self.CC)
        header_bytes.append(self.M << 7 | self.PT)
        header_bytes.append(self.seq_num >> 8)
        header_bytes.append(self.seq_num & 0xFF)

        for i in range(3, -1, -1):
            header_bytes.append((self.timestamp >> (i * 8)) & 0xFF)
        for i in range(3, -1, -1):
            header_bytes.append((self.SSRC >> (i * 8)) & 0xFF)

        if self.CSRC != None:
            header_bytes.append((self.CSRC >> (i * 8)) & 0xFF)

        self.header = bytes(header_bytes)
        if self.X:
            self.header += self.extension_bits

    @classmethod
    def receive(cls, packet: bytes):
        if len(packet) < cls.HEADERSIZE:
            return None

        header = packet[: cls.HEADERSIZE]

        padding = (header[0] >> 5) & 0b1
        ext = bool((header[0] >> 4) & 0b1)
        CSRC_count = header[0] & 0xF
        Marker = (header[1] >> 7) & 0b1
        payload_type = header[1] & 0x7F
        seq_num = (header[2] << 8) | header[3]
        timestamp = (header[4] << 24) | (header[5] << 16) | (header[6] << 8) | header[7]
        SSRC = (header[8] << 24) | (header[9] << 16) | (header[10] << 8) | header[11]

        # if not ext:
        payload = packet[cls.HEADERSIZE :]

        return cls(
            payload_type,
            seq_num,
            timestamp,
            payload,
            padding,
            ext,
            CSRC_count,
            Marker,
            SSRC,
        )

    def get_packet(self) -> bytes:
        return self.header + self.payload
