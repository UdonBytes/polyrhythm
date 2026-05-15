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


def resample_sound(sound, original_sample_rate, target_sample_rate):
    """Match a sample to the app's output sample rate."""
    if original_sample_rate == target_sample_rate:
        return sound

    original_positions = np.arange(len(sound))
    new_length = int(len(sound) * target_sample_rate / original_sample_rate)
    new_positions = np.linspace(0, len(sound) - 1, new_length)

    return np.interp(new_positions, original_positions, sound)


def load_sample(file_name, target_sample_rate=SAMPLE_RATE):
    sound, sample_rate = sf.read(file_name)
    sound = make_mono(sound)
    sound = resample_sound(sound, sample_rate, target_sample_rate)

    return sound


def generate_polyrhythm_audio(
    high_beats,
    low_beats,
    measure_seconds,
    loops,
    muted_high_beats=None,
    muted_low_beats=None,
    tambourine_beats=None,
    hihat_beats=None,
    muted_tambourine_beats=None,
    muted_hihat_beats=None,
    sample_rate=SAMPLE_RATE,
):
    """Create the polyrhythm audio and return WAV bytes."""
    if muted_high_beats is None:
        muted_high_beats = [False] * high_beats

    if muted_low_beats is None:
        muted_low_beats = [False] * low_beats

    if tambourine_beats is not None and muted_tambourine_beats is None:
        muted_tambourine_beats = [False] * tambourine_beats

    if hihat_beats is not None and muted_hihat_beats is None:
        muted_hihat_beats = [False] * hihat_beats

    total_seconds = measure_seconds * loops
    track = np.zeros(int(sample_rate * total_seconds))

    woodblock_high = load_sample("woodblock_high.wav", sample_rate)
    woodblock_low = load_sample("woodblock_low.wav", sample_rate)
    tambourine = None
    hihat = None

    if tambourine_beats is not None:
        tambourine = load_sample("tambourine.wav", sample_rate)
        tambourine = tambourine * 3.0

    if hihat_beats is not None:
        hihat = load_sample("hihat_open.wav", sample_rate)

    downbeat = load_sample("downbeat.wav", sample_rate)

    downbeat = downbeat * 10

    for measure in range(loops):
        measure_start = measure * measure_seconds

        if (
            not muted_high_beats[0]
            or not muted_low_beats[0]
            or (
                muted_tambourine_beats is not None
                and not muted_tambourine_beats[0]
            )
            or (
                muted_hihat_beats is not None
                and not muted_hihat_beats[0]
            )
        ):
            add_sound(track, downbeat, measure_start, sample_rate)

        for i in range(high_beats):
            if muted_high_beats[i]:
                continue

            time = measure_start + i * measure_seconds / high_beats
            add_sound(track, woodblock_high, time, sample_rate)

        for i in range(low_beats):
            if muted_low_beats[i]:
                continue

            time = measure_start + i * measure_seconds / low_beats
            add_sound(track, woodblock_low, time, sample_rate)

        if tambourine_beats is not None:
            for i in range(tambourine_beats):
                if muted_tambourine_beats[i]:
                    continue

                time = measure_start + i * measure_seconds / tambourine_beats
                add_sound(track, tambourine, time, sample_rate)

        if hihat_beats is not None:
            for i in range(hihat_beats):
                if muted_hihat_beats[i]:
                    continue

                time = measure_start + i * measure_seconds / hihat_beats
                add_sound(track, hihat, time, sample_rate)

    max_volume = np.max(np.abs(track))

    if max_volume > 0:
        track = track / max_volume * 0.8

    audio_file = BytesIO()
    sf.write(audio_file, track, sample_rate, format="WAV")
    audio_file.seek(0)

    return audio_file.getvalue()
