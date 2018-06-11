import pitch_to_note
from scipy.io import loadmat
import numpy as np
import math

notes_freqs = list(range(21, 89))
notes_names = [
        "C0", "C#0", "D0", "D#0", "E0", "F0", "F#0", "G0", "G#0", "A0", "A#0",
        "B0",
        "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1",
        "B1",
        "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2",
        "B2",
        "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3",
        "B3",
        "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4",
        "B4",
        "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5",
        "B5",
        "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6",
        "B6",
        "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7",
        "B7",
        "C8", "C#8", "D8", "D#8", "E8", "F8", "F#8", "G8", "G#8", "A8", "A#8",
        "B8"]


def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return array[idx-1]
    else:
        return array[idx]


def pseudoNotes_to_vector(pseudo_notes, amplitudes):
        vector = [0] * len(notes_freqs)
        for i in range(len(vector)):
                j0 = find_nearest(pseudo_notes, i - 1/3)
                j1 = find_nearest(pseudo_notes, i + 1/3)
                vector[i] = surround_to_amplitude(pseudo_notes[j0:j1], amplitudes[j0:j1])
        return vector


def surround_to_amplitude(pseudo_notes, amplitudes):
        amp = 0
        for i in range(len(pseudo_notes)):
                amp += normalized_amplitude(pseudo_notes[i], amplitudes[i])
        amp /= pseudo_notes[-1] - pseudo_notes[0]
        return amp


def normalized_amplitude(note, amp):
        #TODO
        return amp


def normal_note_segment(segment):
        # normal the segment by a window function
        pass


if __name__ == '__main__':
        SMOP_PATH = "C:\\Users\\ohadi\\Desktop\\SMOP"
        # SMOP_PATH = "C:\\Users\\t8554024\\Desktop\\אמיר - תלפיות\\אקדמיה\\אינטרו\\SMOP\\"
        MIDI_file_name = "MIDI//yonatanHakatan.mid"
        # !/usr/bin/env python3
        file_name = 'Weightless.wav'

        file_path = SMOP_PATH + file_name
        x = loadmat(file_name + 'stft.mat')
        s = x['S']
        f = x['f']
        t = x['t']
        vectors = []
        for time in t:
                vectors.append(pseudoNotes_to_vector(f, s[time, :]))
                pass
        pass

