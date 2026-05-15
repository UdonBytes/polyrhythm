import streamlit as st

from audio import generate_polyrhythm_audio
from rhythm import get_measure_seconds
from visualizations import show_animated_timeline, show_polyrhythm_clock


BEATS_PER_MEASURE = 4
LOOPS = 4
MIN_BPM = 40
MAX_BPM = 240
DEFAULT_BPM = 120
MAX_BEATS = 32
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

if "autoplay_after_play" not in st.session_state:
    st.session_state["autoplay_after_play"] = False

if "has_started_playback" not in st.session_state:
    st.session_state["has_started_playback"] = False

if "extra_track_count" not in st.session_state:
    st.session_state["extra_track_count"] = 0

playback_intent = st.query_params.get("playback_intent")

if isinstance(playback_intent, list):
    playback_intent = playback_intent[0]

if playback_intent == "play":
    st.session_state["has_started_playback"] = True
    st.session_state["autoplay_after_play"] = True
elif playback_intent == "pause":
    st.session_state["autoplay_after_play"] = False

current_playback_intent = (
    playback_intent
    if playback_intent in ("play", "pause")
    else ""
)
should_autoplay_audio = (
    st.session_state["has_started_playback"]
    and st.session_state["autoplay_after_play"]
    and current_playback_intent != "pause"
)

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

        .beat-mute-label {{
            font-weight: 600;
            margin-top: 0.8rem;
            margin-bottom: 0.45rem;
        }}

        div[data-testid="stPills"] button {{
            min-width: 2.45rem;
            padding: 0.35rem 0.55rem;
        }}

        div[data-testid="stPills"] button p {{
            line-height: 1.1;
            text-align: center;
            white-space: pre-line;
        }}

        button[kind="pillsActive"] {{
            background: #9ca3af !important;
            background-color: #9ca3af !important;
            border-color: #d1d5db !important;
            box-shadow: 0 0 0 2px rgba(209, 213, 219, 0.45) !important;
        }}

        button[kind="pillsActive"] * {{
            background-color: transparent !important;
        }}

        button[kind="pillsActive"] p {{
            color: #ffffff !important;
            filter: grayscale(1);
            font-weight: 700;
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


def add_extra_track():
    st.session_state["extra_track_count"] = min(
        st.session_state["extra_track_count"] + 1,
        2,
    )


def clear_mute_pills_for_state(state_key):
    for key in list(st.session_state.keys()):
        if key.startswith(f"{state_key}_pills_"):
            del st.session_state[key]


def remove_extra_track():
    if st.session_state["extra_track_count"] == 2:
        st.session_state["muted_hihat_beats"] = []
        clear_mute_pills_for_state("muted_hihat_beats")
        st.session_state.pop("previous_hihat_beat_count", None)
    elif st.session_state["extra_track_count"] == 1:
        st.session_state["muted_tambourine_beats"] = []
        clear_mute_pills_for_state("muted_tambourine_beats")
        st.session_state.pop("previous_tambourine_beat_count", None)

    st.session_state["extra_track_count"] = max(
        st.session_state["extra_track_count"] - 1,
        0,
    )


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


def reset_all_mutes(
    high_beat_count,
    low_beat_count,
    tambourine_beat_count=None,
    hihat_beat_count=None,
):
    st.session_state["muted_high_beats"] = [False] * high_beat_count
    st.session_state["muted_low_beats"] = [False] * low_beat_count
    st.session_state[get_mute_pills_key("muted_high_beats", high_beat_count)] = []
    st.session_state[get_mute_pills_key("muted_low_beats", low_beat_count)] = []

    if tambourine_beat_count is not None:
        st.session_state["muted_tambourine_beats"] = [False] * tambourine_beat_count
        st.session_state[
            get_mute_pills_key("muted_tambourine_beats", tambourine_beat_count)
        ] = []

    if hihat_beat_count is not None:
        st.session_state["muted_hihat_beats"] = [False] * hihat_beat_count
        st.session_state[get_mute_pills_key("muted_hihat_beats", hihat_beat_count)] = []


def get_mute_pills_key(state_key, beat_count):
    return f"{state_key}_pills_{beat_count}"


def sync_mute_state_from_pills(state_key):
    beat_count = len(st.session_state[state_key])
    pills_key = get_mute_pills_key(state_key, beat_count)
    selected_muted_beats = st.session_state.get(pills_key)

    if selected_muted_beats is None:
        return

    selected_muted_set = set(selected_muted_beats)
    st.session_state[state_key] = [
        beat_number in selected_muted_set
        for beat_number in range(1, beat_count + 1)
    ]


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


def update_mutes_from_pills(state_key, beat_count):
    pills_key = get_mute_pills_key(state_key, beat_count)
    selected_muted_beats = st.session_state.get(pills_key) or []
    selected_muted_set = set(selected_muted_beats)

    st.session_state[state_key] = [
        beat_number in selected_muted_set
        for beat_number in range(1, beat_count + 1)
    ]


def show_beat_mute_pills(label, state_key, beat_symbol):
    muted_beats = st.session_state[state_key]
    beat_count = len(muted_beats)
    beat_numbers = list(range(1, beat_count + 1))
    muted_numbers = [
        beat_number
        for beat_number, is_muted in zip(beat_numbers, muted_beats)
        if is_muted
    ]
    pills_key = get_mute_pills_key(state_key, beat_count)

    if pills_key not in st.session_state:
        st.session_state[pills_key] = muted_numbers

    st.markdown(
        f'<div class="beat-mute-label">{label} ({beat_count})</div>',
        unsafe_allow_html=True,
    )
    st.pills(
        f"Muted {label}",
        beat_numbers,
        selection_mode="multi",
        default=muted_numbers,
        format_func=lambda beat_number: f"{beat_symbol} {beat_number}",
        key=pills_key,
        label_visibility="collapsed",
        help="Selected beat numbers are muted.",
        on_change=update_mutes_from_pills,
        args=(state_key, beat_count),
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

use_tambourine = st.session_state["extra_track_count"] >= 1
use_hihat = st.session_state["extra_track_count"] >= 2
tambourine_beats = None
hihat_beats = None
track_columns = [1, 1]

if use_tambourine:
    track_columns.append(1)

if use_hihat:
    track_columns.append(1)

if st.session_state["extra_track_count"] < 2:
    track_columns.append(0.75)

if st.session_state["extra_track_count"] > 0:
    track_columns.append(0.75)

columns = st.columns(track_columns)
high_beats = columns[0].number_input(
    "High Woodblock Beats",
    min_value=1,
    max_value=MAX_BEATS,
    value=2,
)
low_beats = columns[1].number_input(
    "Low Woodblock Beats",
    min_value=1,
    max_value=MAX_BEATS,
    value=3,
)
next_column_index = 2

if use_tambourine:
    tambourine_beats = columns[next_column_index].number_input(
        "Tambourine Beats",
        min_value=1,
        max_value=MAX_BEATS,
        value=4,
    )
    next_column_index += 1

if use_hihat:
    hihat_beats = columns[next_column_index].number_input(
        "Open Hi-Hat Beats",
        min_value=1,
        max_value=MAX_BEATS,
        value=5,
    )
    next_column_index += 1

if st.session_state["extra_track_count"] < 2:
    columns[next_column_index].markdown(
        "<div style='height: 1.75rem'></div>",
        unsafe_allow_html=True,
    )
    columns[next_column_index].button(
        "+ Add More",
        on_click=add_extra_track,
        use_container_width=True,
    )
    next_column_index += 1

if st.session_state["extra_track_count"] > 0:
    columns[next_column_index].markdown(
        "<div style='height: 1.75rem'></div>",
        unsafe_allow_html=True,
    )
    columns[next_column_index].button(
        "- Remove",
        on_click=remove_extra_track,
        use_container_width=True,
    )

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
sync_mute_state_from_pills("muted_high_beats")
sync_mute_state_from_pills("muted_low_beats")

if use_tambourine:
    reset_mutes_when_beat_count_changes(
        "muted_tambourine_beats",
        "previous_tambourine_beat_count",
        tambourine_beats,
    )
    sync_mute_state_from_pills("muted_tambourine_beats")

if use_hihat:
    reset_mutes_when_beat_count_changes(
        "muted_hihat_beats",
        "previous_hihat_beat_count",
        hihat_beats,
    )
    sync_mute_state_from_pills("muted_hihat_beats")

has_muted_beats = (
    any(st.session_state["muted_high_beats"])
    or any(st.session_state["muted_low_beats"])
    or (
        use_tambourine
        and any(st.session_state["muted_tambourine_beats"])
    )
    or (
        use_hihat
        and any(st.session_state["muted_hihat_beats"])
    )
)
with st.expander("Beat Mutes", expanded=False):
    st.button(
        "Reset Mutes",
        disabled=not has_muted_beats,
        use_container_width=True,
        on_click=reset_all_mutes,
        args=(high_beats, low_beats, tambourine_beats, hihat_beats),
    )
    st.caption("Select beat numbers to mute them.")
    show_beat_mute_pills(
        "High Woodblock Beats",
        "muted_high_beats",
        "🔵",
    )
    show_beat_mute_pills(
        "Low Woodblock Beats",
        "muted_low_beats",
        "🔴",
    )
    if use_tambourine:
        show_beat_mute_pills(
            "Tambourine Beats",
            "muted_tambourine_beats",
            "🟡",
        )

    if use_hihat:
        show_beat_mute_pills(
            "Open Hi-Hat Beats",
            "muted_hihat_beats",
            "🟢",
        )

measure_seconds = get_measure_seconds(bpm, "Quarter", BEATS_PER_MEASURE)
audio_bytes = generate_polyrhythm_audio(
    high_beats,
    low_beats,
    measure_seconds,
    LOOPS,
    st.session_state["muted_high_beats"],
    st.session_state["muted_low_beats"],
    tambourine_beats=tambourine_beats,
    hihat_beats=hihat_beats,
    muted_tambourine_beats=(
        st.session_state["muted_tambourine_beats"]
        if use_tambourine
        else None
    ),
    muted_hihat_beats=(
        st.session_state["muted_hihat_beats"]
        if use_hihat
        else None
    ),
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
        tambourine_beats=tambourine_beats,
        hihat_beats=hihat_beats,
        muted_tambourine_beats=(
            st.session_state["muted_tambourine_beats"]
            if use_tambourine
            else None
        ),
        muted_hihat_beats=(
            st.session_state["muted_hihat_beats"]
            if use_hihat
            else None
        ),
        should_autoplay=should_autoplay_audio,
        playback_intent=current_playback_intent,
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
        tambourine_beats=tambourine_beats,
        hihat_beats=hihat_beats,
        muted_tambourine_beats=(
            st.session_state["muted_tambourine_beats"]
            if use_tambourine
            else None
        ),
        muted_hihat_beats=(
            st.session_state["muted_hihat_beats"]
            if use_hihat
            else None
        ),
        should_autoplay=should_autoplay_audio,
        playback_intent=current_playback_intent,
    )
