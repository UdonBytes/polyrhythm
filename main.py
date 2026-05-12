from audio import generate_polyrhythm_audio
from rhythm import get_measure_seconds


BEATS_PER_MEASURE = 4
LOOPS = 4
OUTPUT_FILE_NAME = "rhythm_test.wav"


def main():
    bpm = int(input("Tempo/BPM: "))
    note_type = input("Beat note type (half/quarter/eighth/sixteenth): ").lower()
    high_beats = int(input("High woodblock beats: "))
    low_beats = int(input("Low woodblock beats: "))

    measure_seconds = get_measure_seconds(bpm, note_type, BEATS_PER_MEASURE)
    audio_bytes = generate_polyrhythm_audio(
        high_beats,
        low_beats,
        measure_seconds,
        LOOPS,
    )

    with open(OUTPUT_FILE_NAME, "wb") as audio_file:
        audio_file.write(audio_bytes)

    print(f"Done! Saved {OUTPUT_FILE_NAME}")


if __name__ == "__main__":
    main()
