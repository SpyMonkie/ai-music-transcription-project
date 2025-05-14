# import os
# from music21 import converter, environment

# # Step 1: Set MuseScore Path Automatically
# musescore_path = ""

# if os.name == "nt":  # Windows
#     musescore_path = "C:/Program Files/MuseScore 4/bin/MuseScore4.exe"

# # Configure music21 with MuseScore path
# env = environment.UserSettings()
# env["musicxmlPath"] = musescore_path

# print(f"MuseScore path set to: {musescore_path}")

# # Step 2: Get MIDI file from user
# midi_file = input("Enter the path to the MIDI file: ").strip()

# # Check if the file exists
# if not os.path.exists(midi_file):
#     print("Error: MIDI file not found!")
#     exit()

# # Step 3: Convert MIDI to Sheet Music
# print("\nProcessing MIDI file...")
# score = converter.parse(midi_file)

# # Step 4: Save the Sheet Music
# output_musicxml = 'output/sheet_music.musicxml'
# score.write('musicxml', fp=output_musicxml)
# print(f"Sheet music saved to: {output_musicxml}")

# # Step 5: Save as PDF
# output_pdf = 'output/sheet_music.pdf'
# score.write('pdf', fp=output_pdf)
# print(f"Sheet music saved to: {output_pdf}")

import pretty_midi
from music21 import converter, chord, stream, metadata
import subprocess
import os

def quantize_midi(input_path, output_path, resolution=0.05, min_duration=0.05):
    midi = pretty_midi.PrettyMIDI(input_path)
    for instrument in midi.instruments:
        for note in instrument.notes:
            note.start = round(note.start / resolution) * resolution
            note.end = round(note.end / resolution) * resolution
            if note.end <= note.start:
                note.end = note.start + min_duration
    midi.write(output_path)


# midi_file = "output/The_Way_it_is/piano.wav.midi"
midi_file = "music21test/input_audio/letitgo.midi"
output_path = "music21test/output/letitgo_piano_quantized.midi"
quantize_midi(midi_file, output_path)

# load midi file
score = converter.parse(output_path)

# Flatten to get all notes for chord analysis
flat_score = score.flatten()

# analyze and label chords
chordified = flat_score.chordify()

# analyze chord symbols
for c in chordified.recurse().getElementsByClass('Chord'):
    c.addLyric(c.pitchedCommonName)

outputxml = "music21test/output/letitgo.musicxml"

chordified.metadata = metadata.Metadata()
chordified.metadata.title = "Let It Go"
chordified.metadata.composer = "Kristen Anderson-Lopez, Robert Lopez"

# create a stream for the chord symbols
choridfied = chordified.write('musicxml', fp=outputxml)
output_pdf = "music21test/output/letitgo.pdf"

command = ["musescore4", outputxml, "-o", output_pdf]

subprocess.run(command, check=True)

# # Export without calling makeNotation()
# output_musicxml = 'output/sheet_music.musicxml'
# score.write('musicxml', fp=output_musicxml, makeNotation=True)
# print(f"Sheet music saved to: {output_musicxml}")



