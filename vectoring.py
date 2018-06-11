import pitch_to_note
from scipy.io import loadmat
import numpy as np
import math

NOTE_MARGIN = 1/2
THRESHOLD = 0.1
notes_freqs = list(range(21, 109))
notes_names = [
        "A0", "A#0",
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
        "C8"]


def find_nearest(array, value):
        index = 0
        while index < len(array) and array[index] < value:
                index += 1
        return index


def pseudoNotes_to_vector(pseudo_notes, amplitudes):
        vector = np.zeros(shape=(len(notes_freqs), ))
        count_notes = np.zeros(shape=(len(notes_freqs), ))
        for i in range(len(pseudo_notes)):
                note = -1
                if pseudo_notes[i] == float("-inf"):
                        note = -1
                elif pseudo_notes[i] - math.floor(pseudo_notes[i]) <= NOTE_MARGIN:
                        note = math.floor(pseudo_notes[i])
                elif pseudo_notes[i] - math.floor(pseudo_notes[i]) >= 1 - NOTE_MARGIN:
                        note = math.floor(pseudo_notes[i]) + 1
                if note < 0:
                        continue
                if note >= 109:
                        break
                count_notes[note-notes_freqs[0]] += 1
                vector[note-notes_freqs[0]] += normalized_amplitude(pseudo_notes[i], amplitudes[i], note)
        for note in range(len(vector)):
                if count_notes[note] != 0:
                        vector[note] /= count_notes[note]
                else:
                        vector[note] = 0
        result = vector / np.linalg.norm(vector)
        for i in range(len(result)):
                if result[i] < THRESHOLD:
                        result[i] = 0
        result = result / np.linalg.norm(result)
        return result

def rate_note(note, amplitudes):
        pass


def surround_to_amplitude(pseudo_notes, amplitudes):
        amp = 0
        for i in range(len(pseudo_notes)):
                amp += normalized_amplitude(pseudo_notes[i], amplitudes[i])
        amp /= pseudo_notes[-1] - pseudo_notes[0]
        return amp


def normalized_amplitude(pseudo_note, amp, real_note):
        dist = abs(real_note - pseudo_note)
        normalized_dist = math.e ** (-(NOTE_MARGIN**2)*(dist**2))
        normalized_amp = normalized_dist * amp * math.pow(2, (real_note - notes_freqs[0]) / 12)
        return normalized_amp


def normal_note_segment(segment):
        # normal the segment by a window function
        pass


if __name__ == '__main__':
        SMOP_PATH = "C:\\Users\\ohadi\\Desktop\\SMOP"
        # SMOP_PATH = "C:\\Users\\t8554024\\Desktop\\אמיר - תלפיות\\אקדמיה\\אינטרו\\SMOP\\"
        MIDI_file_name = "MIDI//yonatanHakatan.mid"
        # !/usr/bin/env python3
        file_name = 'Game Show Wheel Spin-SoundBible.com-1305738466.wav'

        file_path = SMOP_PATH + file_name
        x = loadmat(file_name + 'stft.mat')
        s = x['S']
        f = x['f'][0]
        t = x['t'][0]
        vectors = []
        for time in range(len(t)):
                print("time " + str(t[time]) + ": ")
                temp = pseudoNotes_to_vector(f, s[:, time])
                for i in range(len(temp)):
                        if(temp[i] > 0.0):
                                print("\t" + notes_names[i] + ": " + str(temp[i]))
                vectors.append(temp)
                pass
        pass

