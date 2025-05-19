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
from music21 import converter, chord, stream, metadata, meter, tempo, key, midi, harmony
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
quantized_path = "music21test/output/letitgo_piano_quantized.midi"
outputxml = "music21test/output/letitgo.musicxml"
quantize_midi(midi_file, quantized_path)

# Use musescore to convert MIDI to MusicXML for music21
command = ["musescore4", quantized_path, "-o", outputxml]
subprocess.run(command, check=True)


# music21 analysis
score = converter.parse(outputxml)

chordified = score.chordify()

chord_symbols = []
last_offset = -1

for c in chordified.recurse().getElementsByClass('Chord'):
    if c.offset != last_offset:
        try:
            symbol = c.root().name + c.quality
            h = harmony.ChordSymbol()
            h.figure = symbol
            h.quarterLength = 1.0
            h.offset = c.offset
            chord_symbols.append(h)
            last_offset = c.offset
        except Exception as e:
            continue

# main_part = score.parts[0]
# for h in chord_symbols:
#     measure = main_part.measure(h.measureNumber)
#     if measure is not None:
#         print(f"Adding chord symbol {h} to measure {measure.number}")
#         measure.insert(h.offset - measure.offset, h)
main_part = score.parts[0]
for h in chord_symbols:
    main_part.insert(h.offset, h)
    print(f" Offset: {h.offset}, Label: {h.figure}")

score.metadata = metadata.Metadata()
score.metadata.title = "Let It Go"
score.metadata.composer = "Kristen Anderson-Lopez, Robert Lopez"

score.insert(0, meter.TimeSignature('4/4'))
score.insert(0, key.KeySignature(0))

music21_output = "music21test/output/letitgo_chordified.musicxml"
score.write('musicxml', fp=music21_output)

output_pdf = "music21test/output/letitgo.pdf"

command = ["musescore4", music21_output, "-o", output_pdf]

subprocess.run(command, check=True)




