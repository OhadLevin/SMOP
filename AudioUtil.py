import wave
from scipy.io import wavfile
from numpy import array
import warnings
import math

import pyaudio
import sounddevice


FILE = "Berklee44v4/piano_D4.wav"


def slice(startmili, endmili):
    inp = wave.open(FILE, 'rb')
    start = math.
    data = inp.readframes(inp.getnframes() // 2)
    print(data)
    out = wave.open("outTest.wav", 'wb')
    out.setnchannels(inp.getnchannels())
    out.setframerate(inp.getframerate())
    out.setsampwidth(inp.getsampwidth())
    out.writeframes(data)
    inp.close()
    out.close()


def foo():
    a=1
    p = pyaudio.PyAudio()
    p




if __name__ == '__main__':
    warnings.filterwarnings("error")
    slice()
    #foo()

