import pyaudio
import math
import struct
import wave
import time
from datetime import datetime, timedelta
import os

Threshold = 10

SHORT_NORMALIZE = (1.0 / 32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

#TIMEOUT_LENGTH = 15
AUDIO_LENGTH = 0.5 #20
TOTAL_LENGTH = 2 #150



# f_name_directory = r'/home/c2/Desktop/records'

class Recorder:
    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self, f_name_directory):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)
        self.f_name_directory = f_name_directory
        self.current_time = datetime.now()

    def record(self):
        print('Noise detected, recording beginning')
        rec = []
        current = datetime.now()
        end = datetime.now() + timedelta(minutes=AUDIO_LENGTH)

        while current <= end:
            # print(current, type(current))
            # print(end, type(end))
            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold:
                end = datetime.now() + timedelta(minutes=AUDIO_LENGTH)


            current = datetime.now()
            rec.append(data)
        self.write(b''.join(rec))

    def write(self, recording):
        n_files = len(os.listdir(self.f_name_directory))

        filename = os.path.join(self.f_name_directory, '{}.wav'.format(n_files))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        # print('Written to file: {}'.format(filename))
        print('Returning to listening')

    def listen(self):
        print('Listening beginning')
        #while True:
        #nine_hours_from_now = datetime.now() + timedelta(hours=9)
        while datetime.now() < self.current_time + timedelta(minutes=TOTAL_LENGTH):
            # print("Now:", '{:%H:%M:%S}'.format(datetime.now()), "threshold: ", '{:%H:%M:%S}'.format(self.current_time + timedelta(minutes=1)), "Start:", '{:%H:%M:%S}'.format(self.current_time))
            input = self.stream.read(chunk)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                self.record()

# a = Recorder()
# #a.write(f_name_directory)
# a.listen()
