#!/usr/bin/env python

import pyaudio
import socket
import sys
import time
import threading

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
TIME = 0.023219954648526078
# CHUNK = int(RATE*TIME)
CHUNK = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect((sys.argv[1], int(sys.argv[2])))
s.bind((sys.argv[1], int(sys.argv[2])))
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
queue = []
def job():
    try:
        while True:
            start = time.time()
            data = s.recv(CHUNK*2)
            queue.append(data)
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass

thread = threading.Thread(target=job)
thread.start()


while True:
    print(len(queue))
    if len(queue) <= 2:
        time.sleep(0.1)
    else:
        while len(queue):
            data = queue.pop(0)
            # print(data)
            stream.write(data)

print('Shutting down')
s.close()
stream.close()
audio.terminate()
