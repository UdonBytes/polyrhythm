import streamlit as st

from audio import generate_polyrhythm_audio
from rhythm import get_measure_seconds
from visualizations import show_animated_timeline, show_polyrhythm_clock


BEATS_PER_MEASURE = 4
LOOPS = 4
MIN_BPM = 40
MAX_BPM = 240
DEFAULT_BPM = 120
SLIDER_FILL_COLOR = "#8fa3b8"
SLIDER_REST_COLOR = "#f5f5f5"


st.title("Polyrhythm Generator")

if "tempo_bpm" not in st.session_state:
    st.session_state["tempo_bpm"] = DEFAULT_BPM
    st.session_state["tempo_bpm_number"] = DEFAULT_BPM
    st.session_state["tempo_bpm_slider"] = DEFAULT_BPM

tempo_percent = (
    (st.session_state["tempo_bpm"] - MIN_BPM)
    / (MAX_BPM - MIN_BPM)
    * 100
)

st.markdown(
    f"""
    <style>
        div[data-testid="stSlider"],
        div[data-testid="stSlider"] * {{
            color: {SLIDER_REST_COLOR} !important;
        }}

        div[data-testid="stSlider"] [data-baseweb="slider"] div[style="height: 0.25rem;"] {{
            background: linear-gradient(
                to right,
                {SLIDER_FILL_COLOR} 0%,
                {SLIDER_FILL_COLOR} {tempo_percent}%,
                {SLIDER_REST_COLOR} {tempo_percent}%,
                {SLIDER_REST_COLOR} 100%
            ) !important;
        }}

        div[data-testid="stSlider"] [role="slider"] {{
            background: {SLIDER_REST_COLOR} !important;
            border-color: {SLIDER_REST_COLOR} !important;
            box-shadow: 0 0 0 0.2rem rgba(143, 163, 184, 0.35) !important;
            outline-color: {SLIDER_FILL_COLOR} !important;
        }}

        div[data-testid="stSlider"] [role="slider"]:focus,
        div[data-testid="stSlider"] [role="slider"]:focus-visible,
        div[data-testid="stSlider"] [role="slider"]:active {{
            border-color: {SLIDER_FILL_COLOR} !important;
            box-shadow: 0 0 0 0.2rem rgba(143, 163, 184, 0.45) !important;
            outline: 2px solid {SLIDER_FILL_COLOR} !important;
        }}

        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {{
            border-color: {SLIDER_FILL_COLOR} !important;
        }}

        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div[aria-expanded="true"] {{
            border-color: {SLIDER_FILL_COLOR} !important;
            box-shadow: 0 0 0 1px {SLIDER_FILL_COLOR} !important;
            outline-color: {SLIDER_FILL_COLOR} !important;
        }}

        div[data-testid="stSelectbox"] div[data-baseweb="select"] div[style*="rgb(255, 75, 75)"] {{
            border-color: {SLIDER_FILL_COLOR} !important;
            box-shadow: 0 0 0 1px {SLIDER_FILL_COLOR} !important;
            outline-color: {SLIDER_FILL_COLOR} !important;
        }}

        div[data-baseweb="popover"] > div,
        div[data-baseweb="popover"] div[role="listbox"] {{
            border-color: {SLIDER_FILL_COLOR} !important;
        }}

        div[data-testid="stNumberInput"] div[data-baseweb="input"]:hover,
        div[data-testid="stNumberInput"] .focused,
        div[data-testid="stNumberInput"] .focused div[data-baseweb="input"],
        div[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within {{
            border-color: {SLIDER_FILL_COLOR} !important;
            box-shadow: 0 0 0 1px {SLIDER_FILL_COLOR} !important;
            outline-color: {SLIDER_FILL_COLOR} !important;
        }}

        div[data-testid="stNumberInput"] input:focus,
        div[data-testid="stNumberInput"] input:focus-visible {{
            border-color: {SLIDER_FILL_COLOR} !important;
            box-shadow: none !important;
            outline-color: {SLIDER_FILL_COLOR} !important;
        }}

        div[data-testid="stNumberInput"] div[style*="rgb(255, 75, 75)"],
        div[data-testid="stNumberInput"] input[style*="rgb(255, 75, 75)"] {{
            border-color: {SLIDER_FILL_COLOR} !important;
            box-shadow: 0 0 0 1px {SLIDER_FILL_COLOR} !important;
            outline-color: {SLIDER_FILL_COLOR} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


def update_tempo_from_number():
    st.session_state["tempo_bpm"] = st.session_state["tempo_bpm_number"]
    st.session_state["tempo_bpm_slider"] = st.session_state["tempo_bpm_number"]


def update_tempo_from_slider():
    st.session_state["tempo_bpm"] = st.session_state["tempo_bpm_slider"]
    st.session_state["tempo_bpm_number"] = st.session_state["tempo_bpm_slider"]


st.number_input(
    "Tempo/BPM",
    min_value=MIN_BPM,
    max_value=MAX_BPM,
    key="tempo_bpm_number",
    on_change=update_tempo_from_number,
)
st.slider(
    "Tempo/BPM slider",
    min_value=MIN_BPM,
    max_value=MAX_BPM,
    key="tempo_bpm_slider",
    on_change=update_tempo_from_slider,
    label_visibility="collapsed",
)
bpm = st.session_state["tempo_bpm"]
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
