import numpy as np
import pyaudio
import pygame
import pickle
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter, LinearLocator
from mpl_toolkits.mplot3d import Axes3D
from scipy.io import loadmat
import subprocess

import AudioUtil
import recordToMIDI
from pitch_to_note import pitch_to_note
from stft_to_pitch_intervals import stft_to_pitch_interval

SMOP_PATH = "C:\\Users\\t8413244\\Desktop\\SMOP\\"
#SMOP_PATH = "C:\\Users\\t8554024\\Desktop\\אמיר - " \
#            "תלפיות\\אקדמיה\\אינטרו\\SMOP\\"

MIDI_file_name = "MIDI//yonatanHakatan.mid"

#!/usr/bin/env python3
file_name = 'Weightless.wav'

file_path = SMOP_PATH+file_name

python3_command = "C:\\Users\\t8413244\\Desktop\\SMOP\\smopSkeleton.py " \
                  ""+file_path

python3_command = SMOP_PATH + "smopSkeleton.py"
# launch your python2 script using bash

#process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE,
#                           shell= True)

#output, error = process.communicate()  # receive output from the python2
# script
#print(output, error)

x = loadmat(file_name+'stft.mat')
s = x['S']
f = x['f']
t = x['t']

time_pitch_map = {}
count = 0
time = t[0]
current_time_pitches = np.zeros(np.shape(f))
temp = []
temp_amp = []

def find_max_pitch(current_time_pitches):
    return f[np.unravel_index(np.argmax(current_time_pitches, axis=None),
                              current_time_pitches.shape)]

for temp_t in t[0]:
    current_time_pitches += s[:, count]
    count += 1
    time_pitch_map[temp_t] = find_max_pitch(current_time_pitches)
    temp.append((time_pitch_map[temp_t], temp_t))
    temp_amp.append(np.argmax(current_time_pitches,axis=None))
    current_time_pitches = np.zeros(np.shape(f))

max_amp = max(temp_amp)

for i in range(len(temp_amp)):
    if temp_amp[i] < 0.0 * max_amp:
        time_pitch_map[temp[i][1]] = 0
        temp[i] = (0, temp[i][1])
fig = plt.figure()
# ax = fig.gca(projection='3d')
# X, Y = np.meshgrid(t,f)
# Z = Z=np.matrix(s)
# te = np.sin(X+Y)
# my_col = cm.jet(-Z/np.amax(Z))
# surf = ax.plot_surface(X, Y, Z, facecolors= my_col)
# plt.show()
lst_of_intervals = stft_to_pitch_interval(time_pitch_map)

note_in_intervals = {}
for inter in lst_of_intervals:
    note = pitch_to_note(inter[0])
    if(note[0] not in note_in_intervals.keys()):
        note_in_intervals[note[0]] = []
    note_in_intervals[note[0]].append((note[1], inter[1], inter[2]))

for note,inters in note_in_intervals.items():
    inters.sort(key=lambda inter : inter[2]-inter[1])

print(note_in_intervals)
NOTE = "D4"

sliced = AudioUtil.slicer(note_in_intervals[NOTE][-1][1] * 1000,
                        note_in_intervals[NOTE][-1][2] * 1000, file_name)

midi_intervals = recordToMIDI.MIDI_to_tuple(MIDI_file_name)
list_of_files_to_concat = []
for inter in midi_intervals:
    NOTE = inter[0]
    if (NOTE not in note_in_intervals.keys()):
        NOTE = NOTE.replace(NOTE[-1], str(int(NOTE[-1]) + 1))
        if(NOTE not in note_in_intervals.keys()):
            NOTE = NOTE.replace(NOTE[-1], str(int(NOTE[-1])-2))
    sliced = AudioUtil.slicer(note_in_intervals[NOTE][-1][1] * 1000,
                              note_in_intervals[NOTE][-1][2] * 1000, file_name)
    if (inter[2] - inter[1]) <= 0:
        print(inter)
        continue

    sliced = AudioUtil.multiply_by_time(sliced, (inter[2] - inter[1])/1000.0)
    print(inter, sliced)
    temp_tup = (inter, sliced)
    list_of_files_to_concat.append(temp_tup)
list_of_files_to_concat.sort(key= lambda tup:tup[0][1]) # sorting by time
new_list = []
for tup in list_of_files_to_concat:
    new_list.append(tup[1])
concatted = AudioUtil.concat(*new_list)
pygame.init()
pygame.mixer.music.load(concatted)
pygame.mixer.music.play()

plt.plot(t[0], temp[:])
plt.show()