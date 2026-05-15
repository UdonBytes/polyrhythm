# Polyrhythm Generator

Interactive polyrhythm visualization and audio playback tool built with Python and Streamlit.

This project generates customizable layered percussion polyrhythms with synchronized animated visual playback designed for rhythm exploration, practice, and education.

## Live App

https://polyrhythm-generator.streamlit.app/

## Features

* Adjustable BPM
* Up to 4 independent percussion tracks
* Custom polyrhythm generation
* Visual beat subdivision/grouping
* Accented downbeats
* Beat muting system
* Seamless looping playback
* Animated horizontal timeline visualization
* Circular polyrhythm clock visualization
* WAV export/download
* Mobile-friendly layout

## Example Use Cases

* Explore rhythmic relationships such as 3:5, 4:7, or 7:9
* Practice layered percussion timing with synchronized visual playback
* Experiment with beat muting to create syncopated rhythmic patterns
* Slow down complex polyrhythms for practice and internalization
* Visualize pulse alignment using timeline and circular clock modes

## Tech Stack

* Python
* Streamlit
* NumPy
* HTML/CSS/JavaScript visual components

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

## Project Structure

* `app.py`
  Streamlit user interface and app state management

* `audio.py`
  Audio sample loading, mixing, and WAV generation

* `rhythm.py`
  Shared rhythm timing and subdivision calculations

* `timeline.py`
  Animated timeline visualization and playback synchronization

* `main.py`
  Simple command-line version

## Known Limitations

* Streamlit reruns the Python app whenever parameters change, so audio playback currently regenerates from the beginning after interactions
* Rapid parameter changes may temporarily overload websocket updates
* iOS browsers may block autoplay after parameter changes due to browser audio restrictions
* Streamlit Community Cloud may put the app to sleep after inactivity, so the first load may take a moment

## Future Improvements

* Browser-side live playback engine using Web Audio API
* Continuous playback without audio reset
* Improved mobile interaction layout
* More advanced beat grouping and visualization options

## Notes

This project began as a Python-based rhythm generator prototype and gradually evolved into a more interactive audio-visual rhythm exploration tool.