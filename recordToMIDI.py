import mido
from MIDI_to_note import MIDI_to_note

FILE = "MIDI//yonatanHakatan.mid"


def MIDI_to_tuple(mfile):
    inp = mido.MidiFile(mfile)
    tpb = inp.ticks_per_beat
    bpm = 0
    for msg in inp.tracks[0]:
        if msg.type == "set_tempo":
            bpm = tempo_to_bpm(msg.tempo)
    time = 0
    result = []
    temp = []
    temp_result = []
    for msg in inp.tracks[1]:
        if (msg.type == "note_on"):
            time += msg.time
            tmp = (MIDI_to_note(msg.note), ticks_to_miliseconds(time, tpb,
                                                                bpm),
                   ticks_to_miliseconds(time + msg.time, tpb, bpm))
            temp = temp + [(msg.note, time)]
            result.append(tmp)
        elif (msg.type == "note_off"):
            time += msg.time
            for t in temp:
                if t[0] == msg.note:
                    temp.remove(t)
                    temp_result.append((MIDI_to_note(msg.note),
                                        ticks_to_miliseconds(t[1], tpb,
                                                                bpm), ticks_to_miliseconds(time, tpb, bpm)))
                    break
    return temp_result


def ticks_to_miliseconds(ticks, TPB, BPM):
    return 60000 * (ticks / TPB) / BPM



def tempo_to_bpm(tempo):
    return 60000000 / tempo


if __name__=="__main__":
    midi=MIDI_to_tuple(FILE)
    print(midi)
