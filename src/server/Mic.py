import threading
import pyaudio

class Mic:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    TIME = 0.023219954648526078
    CHUNK = 1024

    
    def __init__(self,):
        audio = pyaudio.PyAudio()
        # self.stream = audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,input_device_index=1, frames_per_buffer=self.CHUNK)
        self.stream = audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        self.thread = threading.Thread(target=self.update_frame)
        self.picked = False
        self.thread.start()
    
    def update_frame(self):
        while True:
            data = b''
            # data += b'Sound Start'
            data += self.stream.read(self.CHUNK, exception_on_overflow = True)
            data += b'Sound End'
            self.frame = data
            self.picked = False

    def get_frame(self):
        if self.picked:
            return None
        self.picked = True
        return self.frame

    def close(self):
        self.stream.close()


if __name__ == "__main__":
    import time
    mic = Mic()
    while True:
        print(len(mic.get_frame()))
        time.sleep(0.01)

    mic.close()