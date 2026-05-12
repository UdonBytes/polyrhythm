# Polyrhythm Generator

Python based polyrhythm generator that creates customizable rhythmic audio tracks using layered percussion samples.

## Live App

https://polyrhythm-generator.streamlit.app/

## Features

* Adjustable BPM
* Half, quarter, eighth, and sixteenth note support
* Custom polyrhythms
* Accented downbeats
* Looping playback
* WAV file generation

## How to Run

Install required libraries:

```bash
py -m pip install numpy soundfile
```

Run the program:

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

## Future Plans

* Web interface
* Visual rhythm display
* Custom percussion sounds
* Melodic note playback
* Export options
