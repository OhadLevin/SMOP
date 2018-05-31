import os
import wave
import scipy
import scipy.signal as signal
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import pylab

NUM_OF_PARTS = 1

def stftTest(data, fs):
    # data = a numpy array containing the signal to be processed
    # fs = a scalar which is the sampling frequency of the data
    fft_size = 300
    overlap_fac = 0.5
    hop_size = np.int32(np.floor(fft_size * (1 - overlap_fac)))
    pad_end_size = fft_size  # the last segment can overlap the end of the data array by no more than one window size
    total_segments = np.int32(np.ceil(len(data) / np.float32(hop_size)))
    t_max = len(data) / np.float32(fs)

    window = np.hanning(fft_size)  # our half cosine window
    inner_pad = np.zeros(
        fft_size)  # the zeros which will be used to double each segment size

    proc = np.concatenate(
        (data, np.zeros(pad_end_size)))  # the data to process
    result = np.empty((total_segments, fft_size),
                      dtype=np.float32)  # space to hold the result

    for i in range(total_segments):  # for each segment
        current_hop = hop_size * i  # figure out the current segment offset
        segment = proc[
                  current_hop:current_hop + fft_size]  # get the current segment
        windowed = segment * window  # multiply by the half cosine function
        padded = np.append(windowed,
                           inner_pad)  # add 0s to double the length of the data
        spectrum = np.fft.fft(
            padded) / fft_size  # take the Fourier Transform and scale by the number of samples
        autopower = np.abs(
            spectrum * np.conj(spectrum))  # find the autopower spectrum
        result[i, :] = autopower[:fft_size]  # append to the results array

    result = 20 * np.log10(result)  # scale to db
    result = np.clip(result, -40, 200)  # clip values
    img = plt.imshow(result, origin='lower', cmap='jet',
                     interpolation='nearest', aspect='auto')
    plt.show()

def graph_spectrogram(s, t):
    fft = np.fft.fft(s)
    T = t
    N = s.size

    # 1/T = frequency
    f = np.linspace(0, 1 / T, N)

    x = f[:N // 2]
    y = np.abs(fft)[:N // 2] * 1 / N

    return x,y

def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate

def create_graph(wav_file):
    s, t = get_wav_info(wav_file)
    fig = plt.figure()
    x, y = graph_spectrogram(s, 1 / t)
    plt.plot(x, y)
    maxes = (y.argmax())
    print(y[maxes], x[maxes])
    plt.show()

def stft(x, fs, framesz, hop):
    framesamp = int(framesz*fs)
    hopsamp = int(hop*fs)
    w = scipy.hanning(framesamp)
    X = scipy.array([scipy.fft(w*x[i:i+framesamp])
                     for i in range(0, len(x)-framesamp, hopsamp)])
    return X
if __name__ == '__main__':

    x, fs = get_wav_info('Berklee44v4/piano_Ab4.wav')
    T = x.size / fs
    framesz = 0.0050  # with a frame size of 50 milliseconds
    hop = 0.0025      # and hop size of 25 milliseconds.

    # Create test signal and STFT.
    t = scipy.linspace(0, T, T*fs, endpoint=False)
    X = stft(x, fs, framesz, hop)

    # Plot the magnitude spectrogram.
    pylab.figure()
    pylab.imshow(scipy.absolute(X.T), origin='lower', aspect='auto',
                 interpolation='nearest')
    pylab.xlabel('Time')
    pylab.ylabel('Frequency')
    pylab.show()

