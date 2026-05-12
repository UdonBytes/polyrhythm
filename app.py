import numpy as np
import soundfile as sf
import streamlit as st


def add_sound(track, sound, start_time, sample_rate):
    start_index = int(start_time * sample_rate)
    end_index = start_index + len(sound)

    if end_index > len(track):
        end_index = len(track)
        sound = sound[:end_index - start_index]

    track[start_index:end_index] += sound


st.title("Polyrhythm Generator")

bpm = st.number_input("Tempo/BPM", min_value=40, max_value=240, value=120)
note_type = st.selectbox("Beat note type", ["Half", "Quarter", "Eighth", "Sixteenth"], index=1)
high_beats = st.number_input("High Woodblock Beats", min_value=1, max_value=20, value=2)
low_beats = st.number_input("Low Woodblock Beats", min_value=1, max_value=20, value=3)

if st.button("Generate"):
    sample_rate = 44100

    note_lengths = {
        "half": 2,
        "quarter": 1,
        "eighth": 0.5,
        "sixteenth": 0.25
    }

    note_length = note_lengths[note_type.lower()]

    beats_per_measure = 4
    measure_seconds = beats_per_measure * 60 / bpm * note_length

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

    st.success("Done!")
    st.audio("rhythm_test.wav")