import wave

import time
from scipy.io import wavfile
import math



FILE = "Berklee44v4\\piano_D4.wav"
FILE_OUT = "output\\out-{}.wav"


def slicer(startmili, endmili, file_inputdir):
    file_outdir = FILE_OUT.format(file_inputdir.replace(".wav",
                                                        "").replace("\\",
                                                                    "_") +
                                  "slice-from-" + str(startmili) + "-to-" + str(endmili))
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


def concat(*files):
    file_outdir = FILE_OUT.format("HI".replace(".wav","").replace("\\", "_") +
                                  "concat" + str(time.time()))
    data = b''
    sw = 2
    fr = 44100
    c = 1
    for i in range(len(files)):
        tmp = wave.open(files[i], 'rb')
        data += tmp.readframes(tmp.getnframes())
        c = tmp.getnchannels()
        fr = tmp.getframerate()
        sw = tmp.getsampwidth()
        tmp.close()
    out = wave.open(file_outdir, 'wb')
    out.setnchannels(c)
    out.setframerate(fr)
    out.setsampwidth(sw)
    out.writeframes(data)
    out.close()
    return file_outdir


def multiply(file_in, mult_factor):
    int_factor = math.floor(mult_factor)
    mod_factor = mult_factor - int_factor
    if (int_factor > 0):
        int_arr = [file_in] * int_factor
        file_outtmp = concat(*int_arr)

    file_outdir = FILE_OUT.format(file_in.replace(".wav",
                                                        "").replace("\\",
                                                                    "_") + " mult")
    inp = wave.open(file_in, 'rb')
    inp.rewind()
    dif = math.ceil(inp.getnframes() * mod_factor)
    data = inp.readframes(dif)
    out = wave.open(file_outdir, 'wb')
    out.setnchannels(inp.getnchannels())
    out.setframerate(inp.getframerate())
    out.setsampwidth(inp.getsampwidth())
    out.writeframes(data)
    inp.close()
    out.close()

    if (int_factor > 0):
        file_outdir = concat(file_outtmp, file_outdir)
    return file_outdir


def multiply_by_time(file_in, time):
    inp = wave.open(file_in)
    duration = inp.getnframes() / inp.getframerate()
    print(file_in + " duration " + str(duration))
    inp.close()
    factor = time / duration
    print(" factor " + str(factor))
    return multiply(file_in, factor)




if __name__ == '__main__':
    # #slicer(1000, 2000, FILE)
    f = slicer(1000, 1546, FILE)
    multiply_by_time(f, 502)


