import pyaudio

class Mic:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 4096
    
    def __init__(self,):
        audio = pyaudio.PyAudio()
        self.stream = audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,input_device_index=2, frames_per_buffer=self.CHUNK)

    def get_frame(self):
        data = b''
        # data += b'Sound Start'
        data += self.stream.read(self.CHUNK, exception_on_overflow = False)
        data += b'Sound End'
        return data

    def close(self):
        self.stream.close()


if __name__ == "__main__":
    import time
    mic = Mic()
    while True:
        print(len(mic.get_frame()))
        time.sleep(0.1)

    mic.close()