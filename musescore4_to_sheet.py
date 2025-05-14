import subprocess

# Define the input and output file paths
input_midi = "audio/Die_with_a_smile_drums.wav.midi"
output_pdf = "drums_die_with_a_smile.pdf"

# MuseScore command
command = ["musescore4", input_midi, "-o", output_pdf]

# Run the command
try:
    subprocess.run(command, check=True)
    print(f"Successfully converted {input_midi} to {output_pdf}")
except subprocess.CalledProcessError as e:
    print(f"Error running MuseScore: {e}")
