# Audio Transcription and Sheet Music Generation Tool

This project is a desktop-based tool for transcribing multi-instrument audio into clean sheet music or MIDI. It integrates:
- Source separation with [Spleeter](https://github.com/deezer/spleeter)
- Transcription with [Magenta's Onsets and Frames](https://github.com/magenta/magenta)
- Postprocessing with pretty_midi and MuseScore
- A tkinter GUI for easy control of the pipeline

## Installation Requirements

This project was developed using Python 3.8.20 in an Anaconda environment. To replicate the setup, follow these steps:

### 1. Clone This Repository
```bash
git clone https://github.com/SpyMonkie/ai-music-transcription-project.git
cd ai-music-transcription-project
```

### 2. Install ffmpeg
- Download and install: https://ffmpeg.org/download.html
- Ensure ffmpeg is added to your system PATH.

### 3. Install MuseScore 4
- Download and install: https://musescore.org/en/download
- After installation, make sure MuseScore is accessible from the command line (e.g., `musescore4`).
  - You may need to add the MuseScore binary folder to your PATH.

### 4. Create a Conda Environment
```bash
conda create -n env_name python=3.8.20
conda activate env_name
```

### 5. Install Required Python Dependencies
```bash
pip install -r requirements.txt
```

Alternatively, install manually:
```bash
pip install pretty_midi
pip install music21
pip install spleeter
pip install ffmpeg-python
pip install mido
pip install apache-beam  # only needed if training your own model
```

### 6. Clone and Configure Magenta
This GUI relies on scripts from Magenta's GitHub repository
```bash
git clone https://github.com/magenta/magenta.git
```
The GUI uses some of the python files from their github

> Note: Magenta's Onsets and Frames model requires TensorFlow 1.15.5

```bash
pip install tensorflow==1.15.5
```

## Running the Tool
Once installed, launch the GUI with:
```bash
python gui.py
```

Each step in the pipeline can be run independently:
1. Convert audio to 16kHz mono WAV (if needed)
2. Separate stems with Spleeter
3. Transcribe piano or drums using Magenta
4. Quantize MIDI
5. Export to sheet music PDF with MuseScore

## Repository Structure
```
project-root/
├── gui.py                     # Main GUI launcher
├── magenta/             # magenta github repo
├── requirements.txt          # Python dependencies
```

## Optional: Training Your Own Model
To train a custom Onsets and Frames model:
- Install apache-beam
- Format data using TFRecord (Magenta tools)
- See the official guide: https://github.com/magenta/magenta/blob/main/magenta/models/onsets_frames_transcription/README.md

## License
This project uses the following open-source tools:
- Magenta (Apache License 2.0)
- Spleeter (MIT License)
- MuseScore, pretty_midi, music21, ffmpeg (respective open-source licenses)

See LICENSE.md for attribution and links.

---

Created by Christopher Wu
Senior Project – Cal Poly SLO
2025
