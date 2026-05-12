'''
Created on 2026 May 11

@author: janeh
'''

import numpy as np
import soundfile as sf

def add_sound(track, sound, start_time, sample_rate):
    start_index = int(start_time * sample_rate)
    end_index = start_index + len(sound)

    if end_index > len(track):
        end_index = len(track)
        sound = sound[:end_index - start_index]

    track[start_index:end_index] += sound


sample_rate = 44100

bpm = int(input("Tempo/BPM: "))
note_type = input("Beat note type (half/quarter/eighth/sixteenth): ").lower()

if note_type == "half":
    note_length = 2
elif note_type == "quarter":
    note_length = 1
elif note_type == "eighth":
    note_length = 0.5
elif note_type == "sixteenth":
    note_length = 0.25
else:
    note_length = 1

beats_per_measure = 4

measure_seconds = beats_per_measure * 60 / bpm * note_length

high_beats = int(input("High woodblock beats: "))
low_beats = int(input("Low woodblock beats: "))

loops = 4
total_seconds = measure_seconds * loops

track = np.zeros(int(sample_rate * total_seconds))

woodblock_high, sr1 = sf.read("woodblock_high.wav")
woodblock_low, sr2 = sf.read("woodblock_low.wav")
downbeat, sr3 = sf.read("downbeat.wav")

downbeat = downbeat * 10

if woodblock_high.ndim > 1:
    woodblock_high = woodblock_high[:, 0]

if woodblock_low.ndim > 1:
    woodblock_low = woodblock_low[:, 0]

if downbeat.ndim > 1:
    downbeat = downbeat[:, 0]

for measure in range(loops):
    measure_start = measure * measure_seconds

    add_sound(track, downbeat, measure_start, sample_rate)

    for i in range(high_beats):
        time = measure_start + i * measure_seconds / high_beats
        add_sound(track, woodblock_high, time, sample_rate)

    for i in range(low_beats):
        time = measure_start + i * measure_seconds / low_beats
        add_sound(track, woodblock_low, time, sample_rate)

track = track / np.max(np.abs(track)) * 0.8

sf.write("rhythm_test.wav", track, sample_rate)

print("Done!")