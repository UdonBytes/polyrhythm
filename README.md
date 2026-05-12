# Polyrhythm Generator

Python-based polyrhythm generator that creates customizable layered percussion patterns with animated visual playback.

## Live App

https://polyrhythm-generator.streamlit.app/

## Features

* Adjustable BPM
* Half, quarter, eighth, and sixteenth note support
* Custom polyrhythms
* Accented downbeats
* Seamless looping playback
* Animated beat timeline
* Polyrhythm clock visualization
* WAV download

## How to Run

Install required libraries:

```bash
py -m pip install -r requirements.txt
```

Run the Streamlit app:

```bash
py -m streamlit run app.py
```

You can also run the command-line version:

```bash
py main.py
```

## Example

```text
Tempo/BPM: 120
Beat note type: quarter
High woodblock beats: 3
Low woodblock beats: 5
```

Generates a looping 3:5 polyrhythm audio file.

## Project Structure

* `app.py` - Streamlit user interface
* `audio.py` - audio sample loading and WAV generation
* `rhythm.py` - shared rhythm timing calculations
* `timeline.py` - animated visual timeline and Web Audio playback
* `main.py` - simple command-line version
