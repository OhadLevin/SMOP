import matlab.engine
eng = matlab.engine.start_matlab()
a = eng.stftFunctionToPython('Berklee44v4/piano_Ab5.wav')
s = list(a[0])
f = list(a[1])
t = list(a[2])
print a.size
print s
print f
print t