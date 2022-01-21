#!/usr/bin/env python

import sys
import pyaudio
import socket
import select
import time


import pyaudio
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i))

# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# TIME = 0.023219954648526078
# # CHUNK = int(RATE*TIME)
# CHUNK = 1024

# audio = pyaudio.PyAudio()
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # start Recording
# stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,input_device_index=1, frames_per_buffer=CHUNK)

# # input_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# while True:
#     data = stream.read(CHUNK)
#     print(hash(data))
#     print(len(data))
#     s.sendto(data, (sys.argv[1], int(sys.argv[2])))
#     # time.sleep(TIME)

    

# print("finished recording")

# serversocket.close()
# # stop Recording
# stream.stop_stream()
# stream.close()
# audio.terminate()
