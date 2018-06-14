from mido.backends import pygame

import AudioUtil
import pitch_to_note
from scipy.io import loadmat
from scipy.io.wavfile import write
import numpy as np
import math
from termcolor import colored
import pyaudio
import operator
import time
import random
import pygame

import recordToMIDI

NOTE_MARGIN = 1 / 2
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
DELTA_TIME = 0.1
notes_freq_dict = {21: 27.5, 22: 29.135, 23: 30.868, 24: 32.703}


def note_freq(note):
    n = note - 69
    return 2 ** (n / 12) * 440


def find_nearest(array, value):
    index = 0
    while index < len(array) and array[index] < value:
        index += 1
    return index


def pseudoNotes_to_vector(pseudo_notes, amplitudes):
    vector = np.zeros(shape=(len(notes_freqs),))
    count_notes = np.zeros(shape=(len(notes_freqs),))
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
        count_notes[note - notes_freqs[0]] += 1
        vector[note - notes_freqs[0]] += normalized_amplitude(pseudo_notes[i],
                                                              amplitudes[i],
                                                              note)
    for note in range(len(vector)):
        if count_notes[note] != 0:
            vector[note] /= count_notes[note]
        else:
            vector[note] = 0
    return vector


def normal_and_threshold_vector(vector):
    result = vector / np.linalg.norm(vector)
    for i in range(len(result)):
        if result[i] < THRESHOLD:
            result[i] = 0
    result = result / np.linalg.norm(result)
    return result


def rate_note_temporary(note, amplitudes):
    rate = 0
    freq = note_freq(note + 21)
    # if amplitudes[note] < 2 * amplitudes[note - 1] or amplitudes[note] < 2 *\
    #         amplitudes[note + 1] or amplitudes[note] == 0:
    #     return 0
    num_o_harmonies = 4
    count_harmonies = 0
    for i in range(len(amplitudes)):
        if (is_harmony(freq, note_freq(i + 21))):
            count_harmonies += 1
            # give a rate
            rate += amplitudes[i]
        if count_harmonies >= num_o_harmonies:
            break
    return rate
    pass


def is_harmony(base_note, potential_harmony):
    return abs(round(potential_harmony / base_note) - (potential_harmony
                                                       / base_note)) < 0.02


def surround_to_amplitude(pseudo_notes, amplitudes):
    amp = 0
    for i in range(len(pseudo_notes)):
        amp += normalized_amplitude(pseudo_notes[i], amplitudes[i])
    amp /= pseudo_notes[-1] - pseudo_notes[0]
    return amp


def normalized_amplitude(pseudo_note, amp, real_note):
    dist = abs(real_note - pseudo_note)
    normalized_dist = math.e ** (-(dist ** 2) / (NOTE_MARGIN ** 2))
    normalized_amp = normalized_dist * amp * math.pow(2, (
    real_note - notes_freqs[0]) / 12)
    return normalized_amp


def normal_note_segment(segment):
    # normal the segment by a window function
    pass


def play_vector(vector):
    fs = 44100  # sampling rate, Hz, must be integer
    duration = 0.1  # in seconds, may be float
    samples = np.zeros(int(fs * duration))
    for i in range(len(vector)):
        volume = vector[i]
        f = note_freq(notes_freqs[i])

        # generate samples, note conversion to float32 array
        samples += volume * (np.sin(2 * np.pi * np.arange(0,
                                                          duration,
                                                          1 / fs) * f))
    return samples
    pass

def note_in_each_moment(rates_to_time):
    # rates_to_time is a twi dimensional matrix, first axis is time,
    # and second note, first line is for the notes numbers in MIDI
    note_in_moment = []
    for i in range(1,rates_to_time.shape[0]):
        max_index, max_value = max(enumerate(rates_to_time[i,:]),
                                       key=operator.itemgetter(1))

        best_note = 1
        for j in range(0, rates_to_time.shape[1]):
            RATIO = 2
            for k in range(0, rates_to_time.shape[1]):
                if (j == k):
                    continue
                if rates_to_time[i, j] < RATIO * rates_to_time[i, k]: #bad
                    if j < k:
                        if is_harmony(j+21, k+21):
                            continue
                        else:
                            break
                    else:
                        break
            else:
                best_note = j
                break
        if best_note != -1:
            note_in_moment.append(rates_to_time[0, best_note])
        else:
            note_in_moment.append(-1)
    return note_in_moment

def for_moment_to_intervals(note_in_moment):
    intervals = []
    lst = []
    last_note = note_in_moment[0]
    current_interval = [last_note, 0, 0]
    for t in range(len(note_in_moment)):
        if note_in_moment[t] == last_note:
            current_interval[2] = DELTA_TIME * (t+1)
        else:
            intervals.append(current_interval)
            last_note = note_in_moment[t]
            current_interval = [last_note, DELTA_TIME * t, DELTA_TIME * t]
    intervals.append(current_interval)
    return intervals

def intervals_list_to_dictionary(intervals_lst):
    intervals_dict = {}
    for inter in intervals_lst:
        if inter[0] not in intervals_dict.keys():
            intervals_dict[inter[0]] = [inter]
        else:
            intervals_dict[inter[0]].append(inter)
    return intervals_dict

def intervals_passing_length(intervals, length):
    passing = []
    for interval in intervals:
        if interval[2] - interval[1] > length:
            passing.append(interval)
    return passing

if __name__ == '__main__':

    p = pyaudio.PyAudio()
    SMOP_PATH = "C:\\Users\\ohadi\\Desktop\\SMOP"
    # SMOP_PATH = "C:\\Users\\t8554024\\Desktop\\אמיר - תלפיות\\אקדמיה\\אינטרו\\SMOP\\"
    MIDI_file_name = "MIDI//yonatanHakatan.mid"
    # !/usr/bin/env python3
    directory = ''
    file_name = "c4toc5_1.m4a"
    fs = 44100  # sampling rate, Hz, must be integer

    file_path = SMOP_PATH + file_name
    x = loadmat(directory + file_name + 'stft.mat')
    s = x['S']
    f = x['f'][0]
    t = x['t'][0]
    vectors = []
    count = 0
    rates_to_time = np.array(list(range(21,109)), ndmin=2) # an array that stores for each
    # time the rates of each note
    samples = np.array([])
    for time_1 in range(len(t)):
        print("time " + str(t[time_1]) + ": ")
        temp = pseudoNotes_to_vector(f, s[:, time_1])
        samples = np.concatenate((samples, play_vector(temp)))
        normalized = normal_and_threshold_vector(temp)
        rates = []
        for i in range(len(temp)):
            temp_rate = rate_note_temporary(i, normalized)
            rates.append(temp_rate)
            # if (normalized[i] > 0.0):
            #     if normalized[i] > 0.6:
            #         print(colored(
            #             "\t amp: " + notes_names[i] + ": " + str(normalized[
            #                                                          i]),
            #             'red'))
            #     else:
            #         print("\t amp: " + notes_names[i] + ": " + str(normalized[i]))
            #
            # if (temp_rate > 0.0 and normalized[i] > 0.0):
            #     if temp_rate > 0.6:
            #         print(colored(
            #             "\t\t rate: " + notes_names[i] + ": " + str(temp_rate),
            #             'magenta'))
            #     else:
            #         print("\t\t rate: " + notes_names[i] + ": " + str(
            #             temp_rate))
        max_index, max_value = max(enumerate(rates),
                                   key=operator.itemgetter(1))
        arr = np.array([rates])
        rates_to_time = np.concatenate((rates_to_time, arr))
        vectors.append(temp)
    note_in_time = note_in_each_moment(rates_to_time)
    notes_intervals = for_moment_to_intervals(note_in_time)
    notes_intervals_dict = intervals_list_to_dictionary(notes_intervals)
    midi_intervals = recordToMIDI.MIDI_to_tuple(MIDI_file_name)

    list_of_files_to_concat = []
    for midi_interval in midi_intervals:
        midi_note = notes_freqs[notes_names.index(midi_interval[0])]
        if midi_note not in notes_intervals_dict.keys():
            print(colored("there is no " + midi_interval[0] + " note in the recording",'red'))
            exit()
        intervals_in_recording = notes_intervals_dict[midi_note]
        passing_intervals = intervals_passing_length(intervals_in_recording, midi_interval[2] - midi_interval[1])
        chosen_interval_in_recording = random.choice(passing_intervals)
        sliced = AudioUtil.slicer(chosen_interval_in_recording[1] * 1000,
                                  chosen_interval_in_recording[2] * 1000, file_name)

        temp_tup = (midi_interval, sliced)
        list_of_files_to_concat.append(temp_tup)
        pass
    list_of_files_to_concat.sort(key=lambda tup: tup[0][1])  # sorting by time
    new_list = []
    for tup in list_of_files_to_concat:
        new_list.append(tup[1])
    concatted = AudioUtil.concat(*new_list)
    pygame.init()
    pygame.mixer.music.load(concatted)
    pygame.mixer.music.play()


    samples = np.int16(samples * 32767)
    write('test' + file_name + '.wav', fs, samples)
    pass

