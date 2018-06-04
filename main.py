import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter, LinearLocator
from mpl_toolkits.mplot3d import Axes3D
from scipy.io import loadmat
import subprocess

import AudioUtil
from pitch_to_note import pitch_to_note
from stft_to_pitch_intervals import stft_to_pitch_interval

SMOP_PATH = "C:\\Users\\t8413244\\Desktop\\SMOP\\"
#SMOP_PATH = "C:\\Users\\t8554024\\Desktop\\אמיר - " \
#            "תלפיות\\אקדמיה\\אינטרו\\SMOP\\"


#!/usr/bin/env python3
file_name = 'Berklee44v4\\piano_D4.wav'

file_path = SMOP_PATH+file_name
python3_command = "C:\\Users\\t8413244\\Desktop\\SMOP\\smopSkeleton.py " \
                  ""+file_path  #
python3_command = SMOP_PATH + "\\smopSkeleton.py"
# launch your python2 script using bash

process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE,
                           shell= True)
output, error = process.communicate()  # receive output from the python2 script



x = loadmat(file_path+'stft.mat')
s = x['S']
f = x['f']
t = x['t']

time_pitch_map = {}
count = 0
time = t[0]
current_time_pitches = np.zeros(np.shape(f))
temp = []
temp_amp = []
for temp_t in t[0]:

    current_time_pitches += s[:, count]
    count += 1
    time_pitch_map[temp_t] = f[np.unravel_index(np.argmax(
        current_time_pitches,axis=None), current_time_pitches.shape)]
    temp.append((time_pitch_map[temp_t], temp_t))
    temp_amp.append(np.argmax(current_time_pitches,axis=None))
    current_time_pitches = np.zeros(np.shape(f))

max_amp = max(temp_amp)

for i in range(len(temp_amp)):
    if temp_amp[i] < 0.0 * max_amp:
        time_pitch_map[temp[i][1]] = 0
        temp[i] = (0, temp[i][1])
print(time_pitch_map)

fig = plt.figure()
# ax = fig.gca(projection='3d')
# X, Y = np.meshgrid(t,f)
# Z = Z=np.matrix(s)
# te = np.sin(X+Y)
# my_col = cm.jet(-Z/np.amax(Z))
# surf = ax.plot_surface(X, Y, Z, facecolors= my_col)
# plt.show()
lst_of_intervals = stft_to_pitch_interval(time_pitch_map)
for inter in lst_of_intervals:
    print(str(pitch_to_note(inter[0])) + " from: " + str(inter[1]) + " to: " +
          str(inter[2]))

note_in_intervals = {}
for inter in lst_of_intervals:
    note = pitch_to_note(inter[0])
    if(note[0] not in note_in_intervals.keys()):
        note_in_intervals[note[0]] = []
    note_in_intervals[note[0]].append((note[1], inter[1], inter[2]))
print(note_in_intervals)

for note,inters in note_in_intervals.items():
    inters.sort(key=lambda inter : inter[2]-inter[1])

print(note_in_intervals)
NOTE = "D5"

print(note_in_intervals[NOTE][-1][1],note_in_intervals[NOTE][-1][2], file_path)

AudioUtil.slicer(note_in_intervals[NOTE][-1][1] * 1000,note_in_intervals[
    NOTE][-1][2] * 1000, file_name)
plt.plot(t[0], temp[:])
plt.show()