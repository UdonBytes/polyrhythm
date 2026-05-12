import streamlit as st

from audio import generate_polyrhythm_audio
from rhythm import get_measure_seconds
from timeline import show_animated_timeline, show_polyrhythm_clock


BEATS_PER_MEASURE = 4
LOOPS = 4


st.title("Polyrhythm Generator")

bpm = st.number_input("Tempo/BPM", min_value=40, max_value=240, value=120)
note_type = st.selectbox("Beat note type", ["Half", "Quarter", "Eighth", "Sixteenth"], index=1)
high_beats = st.number_input("High Woodblock Beats", min_value=1, max_value=20, value=2)
low_beats = st.number_input("Low Woodblock Beats", min_value=1, max_value=20, value=3)
visualization = st.selectbox(
    "Visualization",
    ["Horizontal timeline", "Polyrhythm clock"],
)

if st.button("Generate"):
    measure_seconds = get_measure_seconds(bpm, note_type, BEATS_PER_MEASURE)
    audio_bytes = generate_polyrhythm_audio(
        high_beats,
        low_beats,
        measure_seconds,
        LOOPS,
    )

    st.session_state["generated_rhythm"] = {
        "audio_bytes": audio_bytes,
        "high_beats": high_beats,
        "low_beats": low_beats,
        "measure_seconds": measure_seconds,
    }

if "generated_rhythm" in st.session_state:
    rhythm = st.session_state["generated_rhythm"]

    st.success("Done!")

    if visualization == "Horizontal timeline":
        show_animated_timeline(
            rhythm["high_beats"],
            rhythm["low_beats"],
            BEATS_PER_MEASURE,
            rhythm["measure_seconds"],
            rhythm["audio_bytes"],
        )
    else:
        show_polyrhythm_clock(
            rhythm["high_beats"],
            rhythm["low_beats"],
            BEATS_PER_MEASURE,
            rhythm["measure_seconds"],
            rhythm["audio_bytes"],
        )

    st.download_button(
        label="Download WAV",
        data=rhythm["audio_bytes"],
        file_name="polyrhythm.wav",
        mime="audio/wav",
        on_click="ignore",
    )
