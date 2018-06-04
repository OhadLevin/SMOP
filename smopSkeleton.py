import matlab.engine
import sys
eng = matlab.engine.start_matlab()
a = eng.stftFunctionToPython(sys.argv[0])
print("done matlab")