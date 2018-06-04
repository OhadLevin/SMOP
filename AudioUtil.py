import wave
from scipy.io import wavfile
import math



FILE = "Berklee44v4\\piano_D4.wav"
FILE_OUT = "output\\out-{}.wav"


def slicer(startmili, endmili, file_inputdir):
    file_outdir = FILE_OUT.format(file_inputdir.replace(".wav","").replace(
        "\\", "_") + "_from_" + str(startmili) + "_to_" + str(endmili))
    inp = wave.open(file_inputdir, 'rb')
    fr = inp.getframerate()
    start = math.floor(startmili * fr / 1000)
    end = math.ceil(endmili * fr / 1000)
    dif = end - start
    inp.rewind()
    inp.setpos(start)
    data = inp.readframes(dif)
    out = wave.open(file_outdir, 'wb')
    out.setnchannels(inp.getnchannels())
    out.setframerate(inp.getframerate())
    out.setsampwidth(inp.getsampwidth())
    out.writeframes(data)
    inp.close()
    out.close()
    return file_outdir



if __name__ == '__main__':
    slicer(1000, 2000, FILE)

