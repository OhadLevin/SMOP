ERROR_SIZE = 0


def stft_to_pitch_interval(max_pitch_to_time_map):
    lst = []
    current_interval = [0, 0, 0]
    for time, pitch in max_pitch_to_time_map.items():
        if equal_to_error(pitch, current_interval[0]):
            current_interval[2] = time
        else:
            lst.append(tuple(current_interval))
            current_interval = [pitch, time, time]

    return lst


def equal_to_error(first, second):
    return abs(first - second) <= ERROR_SIZE
