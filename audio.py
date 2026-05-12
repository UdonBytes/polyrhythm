from io import BytesIO

import numpy as np
import soundfile as sf


SAMPLE_RATE = 44100


def add_sound(track, sound, start_time, sample_rate):
    start_index = int(start_time * sample_rate)
    end_index = start_index + len(sound)

    if end_index > len(track):
        end_index = len(track)
        sound = sound[:end_index - start_index]

    track[start_index:end_index] += sound


def make_mono(sound):
    """Use the first channel when a sample is stereo."""
    if sound.ndim > 1:
        return sound[:, 0]

    return sound


def load_sample(file_name):
    sound, sample_rate = sf.read(file_name)
    return make_mono(sound), sample_rate


def generate_polyrhythm_audio(
    high_beats,
    low_beats,
    measure_seconds,
    loops,
    sample_rate=SAMPLE_RATE,
):
    """Create the polyrhythm audio and return WAV bytes."""
    total_seconds = measure_seconds * loops
    track = np.zeros(int(sample_rate * total_seconds))

    woodblock_high, sr1 = load_sample("woodblock_high.wav")
    woodblock_low, sr2 = load_sample("woodblock_low.wav")
    downbeat, sr3 = load_sample("downbeat.wav")

    downbeat = downbeat * 10

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

    audio_file = BytesIO()
    sf.write(audio_file, track, sample_rate, format="WAV")
    audio_file.seek(0)

    return audio_file.getvalue()
