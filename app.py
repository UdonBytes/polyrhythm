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
SUBDIVISION_OPTIONS = {
    "None": 0,
    "Halves": 2,
    "Quarters": 4,
}


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

        div[data-testid="stSlider"]:has([aria-label="Tempo/BPM Slider"]) [data-baseweb="slider"] div[style="height: 0.25rem;"] {{
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

        div[data-testid="stHorizontalBlock"]:has(#beat-mutes-heading) {{
            align-items: flex-start;
        }}

        div[data-testid="stHorizontalBlock"]:has(#beat-mutes-heading) h3 {{
            margin-top: 0;
            margin-bottom: 0;
        }}

        div[data-testid="stHorizontalBlock"]:has(#beat-mutes-heading) button {{
            margin-top: 2.05rem;
            min-height: 2.25rem;
            padding: 0.25rem 0.8rem;
            white-space: nowrap;
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


def reset_mutes_when_beat_count_changes(state_key, count_key, beat_count):
    """Reset mutes when the generated beat count changes."""
    current_mutes = st.session_state.get(state_key, [])
    previous_count = st.session_state.get(count_key)

    if previous_count != beat_count or len(current_mutes) != beat_count:
        st.session_state[state_key] = [False] * beat_count
        st.session_state[count_key] = beat_count


def toggle_beat_mute(state_key, beat_index):
    st.session_state[state_key][beat_index] = (
        not st.session_state[state_key][beat_index]
    )


def reset_all_mutes(high_beat_count, low_beat_count):
    st.session_state["muted_high_beats"] = [False] * high_beat_count
    st.session_state["muted_low_beats"] = [False] * low_beat_count


def show_beat_mute_buttons(label, state_key, beat_count):
    st.write(label)

    for row_start in range(0, beat_count, 10):
        row_end = min(row_start + 10, beat_count)
        columns = st.columns(row_end - row_start)

        for column, beat_index in zip(columns, range(row_start, row_end)):
            is_muted = st.session_state[state_key][beat_index]
            button_label = "○" if is_muted else "●"
            help_text = f"Toggle Beat {beat_index + 1}"

            column.button(
                button_label,
                key=f"{state_key}_{beat_index}",
                help=help_text,
                use_container_width=True,
                on_click=toggle_beat_mute,
                args=(state_key, beat_index),
            )


st.number_input(
    "Tempo/BPM",
    min_value=MIN_BPM,
    max_value=MAX_BPM,
    key="tempo_bpm_number",
    on_change=update_tempo_from_number,
)
st.slider(
    "Tempo/BPM Slider",
    min_value=MIN_BPM,
    max_value=MAX_BPM,
    key="tempo_bpm_slider",
    on_change=update_tempo_from_slider,
    label_visibility="collapsed",
)
bpm = st.session_state["tempo_bpm"]
high_beats = st.number_input("High Woodblock Beats", min_value=1, max_value=20, value=2)
low_beats = st.number_input("Low Woodblock Beats", min_value=1, max_value=20, value=3)
visualization = st.selectbox(
    "Visualization",
    ["Horizontal Timeline", "Polyrhythm Clock"],
)
subdivision_guides = st.selectbox(
    "Subdivision Guides",
    list(SUBDIVISION_OPTIONS.keys()),
    index=0,
)

reset_mutes_when_beat_count_changes(
    "muted_high_beats",
    "previous_high_beat_count",
    high_beats,
)
reset_mutes_when_beat_count_changes(
    "muted_low_beats",
    "previous_low_beat_count",
    low_beats,
)

has_muted_beats = any(st.session_state["muted_high_beats"]) or any(
    st.session_state["muted_low_beats"]
)
mute_heading, mute_reset = st.columns([4, 1.4])
mute_heading.markdown(
    '<span id="beat-mutes-heading"></span><h3>Beat Mutes</h3>',
    unsafe_allow_html=True,
)
mute_reset.button(
    "Reset Mutes",
    disabled=not has_muted_beats,
    use_container_width=True,
    on_click=reset_all_mutes,
    args=(high_beats, low_beats),
)
show_beat_mute_buttons(
    "High Woodblock Beats",
    "muted_high_beats",
    high_beats,
)
show_beat_mute_buttons(
    "Low Woodblock Beats",
    "muted_low_beats",
    low_beats,
)

measure_seconds = get_measure_seconds(bpm, "Quarter", BEATS_PER_MEASURE)
audio_bytes = generate_polyrhythm_audio(
    high_beats,
    low_beats,
    measure_seconds,
    LOOPS,
    st.session_state["muted_high_beats"],
    st.session_state["muted_low_beats"],
)

if visualization == "Horizontal Timeline":
    show_animated_timeline(
        high_beats,
        low_beats,
        BEATS_PER_MEASURE,
        measure_seconds,
        audio_bytes,
        SUBDIVISION_OPTIONS[subdivision_guides],
        st.session_state["muted_high_beats"],
        st.session_state["muted_low_beats"],
    )
else:
    show_polyrhythm_clock(
        high_beats,
        low_beats,
        BEATS_PER_MEASURE,
        measure_seconds,
        audio_bytes,
        SUBDIVISION_OPTIONS[subdivision_guides],
        st.session_state["muted_high_beats"],
        st.session_state["muted_low_beats"],
    )

st.download_button(
    label="Download WAV",
    data=audio_bytes,
    file_name="polyrhythm.wav",
    mime="audio/wav",
    on_click="ignore",
)
