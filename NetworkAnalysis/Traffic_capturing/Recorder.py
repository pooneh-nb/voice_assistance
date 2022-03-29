import pyaudio
import math
import struct
import wave
import time
import os

# https://stackoverflow.com/questions/18406570/python-record-audio-on-detected-sound
Threshold = 15
SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2
TIMEOUT_LENGTH = 5

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

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    def record(self, file_name):
        print('Noise detected, recording now')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        default_end = time.time() + 30
        force_stop = False

        while current <= end:
            data = self.stream.read(chunk)

            if self.rms(data) >= Threshold:
                end = time.time() + TIMEOUT_LENGTH

            current = time.time()
            rec.append(data)

            # stop recording after 30 seconds
            if current > default_end:
                force_stop = True
                break

        self.write(b''.join(rec), file_name)

        return force_stop

    def write(self, recording, file_name):
        time_1 = os.path.getmtime(file_name + '-1.wav')
        time_2 = os.path.getmtime(file_name + '-2.wav')

        if time_1 > time_2:
            file_name = file_name + '-2.wav'
        else:
            file_name = file_name + '-1.wav'

        wf = wave.open(file_name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        print('Written to file: {}'.format(file_name))
        print('Listening again')

    def listen(self, file_name):
        count = 0
        speak_counter = 0
        force_stop = False

        while True:
            input = self.stream.read(chunk)
            rms_val = self.rms(input)

            # May need to move this logic up in write.
            if rms_val >= Threshold:
                count = 0
                speak_counter += 1

                ## 6 * 5 (TIMEOUT)
                ## Listen for 30 seconds at max and then break
                if speak_counter > 6:
                   force_stop = True
                   break

                force_stop = self.record(file_name)

                if force_stop:
                    break

            elif rms_val < Threshold:
                count += 1
                if count > 30:
                    break

        return force_stop