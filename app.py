import streamlit as st

from audio import generate_polyrhythm_audio
from rhythm import get_measure_seconds
from timeline import show_animated_timeline


BEATS_PER_MEASURE = 4
LOOPS = 4


st.title("Polyrhythm Generator")

bpm = st.number_input("Tempo/BPM", min_value=40, max_value=240, value=120)
note_type = st.selectbox("Beat note type", ["Half", "Quarter", "Eighth", "Sixteenth"], index=1)
high_beats = st.number_input("High Woodblock Beats", min_value=1, max_value=20, value=2)
low_beats = st.number_input("Low Woodblock Beats", min_value=1, max_value=20, value=3)

if st.button("Generate"):
    measure_seconds = get_measure_seconds(bpm, note_type, BEATS_PER_MEASURE)
    audio_bytes = generate_polyrhythm_audio(
        high_beats,
        low_beats,
        measure_seconds,
        LOOPS,
    )

    st.success("Done!")
    show_animated_timeline(
        high_beats,
        low_beats,
        BEATS_PER_MEASURE,
        measure_seconds,
        audio_bytes,
    )

    st.download_button(
        label="Download WAV",
        data=audio_bytes,
        file_name="polyrhythm.wav",
        mime="audio/wav",
        on_click="ignore",
    )
