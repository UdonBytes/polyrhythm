NOTE_LENGTHS = {
    "half": 2,
    "quarter": 1,
    "eighth": 0.5,
    "sixteenth": 0.25,
}


def get_note_length(note_type):
    """Convert a note type name into its length in beats."""
    return NOTE_LENGTHS.get(note_type.lower(), 1)


def get_measure_seconds(bpm, note_type, beats_per_measure):
    """Return how many seconds one measure lasts."""
    note_length = get_note_length(note_type)
    return beats_per_measure * 60 / bpm * note_length


def get_beat_marker_positions(number_of_beats, beats_per_measure):
    """Return beat marker positions as percentages across the measure."""
    beat_spacing = beats_per_measure / number_of_beats
    beat_positions = []

    for i in range(number_of_beats):
        beat_position = i * beat_spacing
        beat_percent = beat_position / beats_per_measure * 100
        beat_positions.append(beat_percent)

    return beat_positions
