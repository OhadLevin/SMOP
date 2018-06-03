import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter, LinearLocator
from mpl_toolkits.mplot3d import Axes3D
from scipy.io import loadmat

SMOP_PATH = "C:\\Users\\t8413244\\Desktop\\SMOP\\"
TIME_PERIOD = 0.05 # time period to get an average pitch of

######### get data from file
s = []
f = []
t = []
# with open(SMOP_PATH+"s.txt", "rb") as fp:
#     s = pickle.load(fp)
# with open(SMOP_PATH+"f.txt", "rb") as fp:
#     f = pickle.load(fp)
# with open(SMOP_PATH+"t.txt", "rb") as fp:
#     t = pickle.load(fp)

x = loadmat(SMOP_PATH+'c4toc5_1.m4a'
            'stft'
            '.mat')
s = x['S']
f= x['f']
t = x['t']

time_pitch_map = {}
count = 0
time = t[0]
current_time_pitches = np.zeros(np.shape(f))
count_runs = 1
total_runs = 0
temp = []
temp_amp = []
for temp_t in t[0]:

    current_time_pitches += s[:,total_runs]
    count_runs +=1
    total_runs += 1
    if(True):
        count+=1
        current_time_pitches /= count_runs
        time_pitch_map[count* TIME_PERIOD] = f[np.unravel_index(np.argmax(
            current_time_pitches,axis=None), current_time_pitches.shape)]
        temp.append(time_pitch_map[count* TIME_PERIOD])

        temp_amp.append(np.argmax(current_time_pitches,axis=None))
        current_time_pitches = np.zeros(np.shape(f))
        count_runs = 0

max_amp = max(temp_amp)
print(max_amp)
print(temp_amp)
for i in range(len(temp_amp)):
    if(temp_amp[i] < 0.2*max_amp):
        print(temp_amp[i])
        temp[i] = 0
print(time_pitch_map)

fig = plt.figure()
# ax = fig.gca(projection='3d')
# X, Y = np.meshgrid(t,f)
# Z = Z=np.matrix(s)
# te = np.sin(X+Y)
# my_col = cm.jet(-Z/np.amax(Z))
# surf = ax.plot_surface(X, Y, Z, facecolors= my_col)
# plt.show()
plt.plot(temp)
plt.show()