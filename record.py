import pyaudio

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 41000
RECORD_SECONDS = 5


p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = chunk)



print ("***Recording***")

a = [] 

for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
    data = stream.read(chunk)
    a.append(data) 


print("***Stop recording***")


print ("***START PLAY***")

data = b''.join(a)

for i in range(0, len(data), chunk):
    stream.write(data[i:i+chunk])