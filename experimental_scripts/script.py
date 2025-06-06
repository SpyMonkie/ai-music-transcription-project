import os
import shutil
import subprocess
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

# Function to get user input with tab-completion and option to skip
def get_file_path(prompt_text, allow_skip=True):
    user_input = prompt(
        prompt_text + (" (Press Enter to skip): " if allow_skip else ""),
        completer=PathCompleter(),
        complete_while_typing=True
    ).strip()
    return user_input if user_input else None  # Return None if skipped

# Step 1: Get the input audio file
input_audio = get_file_path("Enter the path to the original input audio file: ", allow_skip=False)

# Step 2: Convert input audio to 16-bit, 16kHz mono WAV
converted_audio = get_file_path("Enter the path where the converted (16kHz WAV) file should be saved (include .wav name): ")
if converted_audio:
    print(f"\nConverting audio to 16kHz mono WAV...\nSaving to: {converted_audio}")
    ffmpeg_command = f'ffmpeg -i "{input_audio}" -ar 16000 -ac 1 "{converted_audio}"'
    os.system(ffmpeg_command)
    print(f"Converted file saved at: {converted_audio}")
else:
    converted_audio = input_audio  # If skipped, assume input is already converted

# Step 3: Perform source separation using Spleeter
spleeter_output = get_file_path("\nEnter the directory where separated stems should be saved: ")
if spleeter_output:
    print(f"\nPerforming source separation with Spleeter...\nSaving stems in: {spleeter_output}")
    spleeter_command = f'spleeter separate -p spleeter:5stems -o "{spleeter_output}" "{converted_audio}"'
    os.system(spleeter_command)
    print(f"Separated stems saved at: {spleeter_output}")

# Step 4: Prompt for final output directory for Magenta
final_output_dir = get_file_path("\nEnter the directory where the Magenta output should be saved: ")
if not final_output_dir:
    print("No output directory provided. Skipping transcription.")
    exit()

# Step 5: Get the piano stem file (or skip)
piano_audio = get_file_path("\nEnter the path to the extracted piano stem (usually inside the separated folder): ")
if not piano_audio:
    print("No piano stem provided. Skipping transcription.")
    exit()

# Step 6: Create a subdirectory in the output directory
output_subdir = os.path.join(final_output_dir, os.path.splitext(os.path.basename(converted_audio))[0])
os.makedirs(output_subdir, exist_ok=True)

# Step 7: Copy piano stem into the new output directory
piano_copy_path = os.path.join(output_subdir, os.path.basename(piano_audio))
shutil.copy(piano_audio, piano_copy_path)
print(f"Copied piano stem to: {piano_copy_path}")

# Step 8: Run Magenta transcription
print(f"\nRunning Magenta onset transcription...\nSaving MIDI to: {output_subdir}")
# magenta_command = (
#     f"python magenta/magenta/models/onsets_frames_transcription/onsets_frames_transcription_transcribe.py "
#     f"--model_dir=./maestro_checkpoint/train "
#     f'"{piano_copy_path}"'
# )

magenta_command = (
    f"python magenta/magenta/models/onsets_frames_transcription/onsets_frames_transcription_transcribe.py "
    f"--config=drums "
    f"--model_dir=./maestro_checkpoint/drum "
    f'"{piano_copy_path}"'
)


os.system(magenta_command)

input_midi = get_file_path("\nEnter the path to the MIDI file: ")
output_pdf = get_file_path("Enter the path to the output PDF file (include pdf name): ")
command = ["musescore4", input_midi, "-o", output_pdf]

try:
    subprocess.run(command, check=True)
    print(f"Successfully converted {input_midi} to {output_pdf}")
except subprocess.CalledProcessError as e:
    print(f"Error running MuseScore: {e}")

print("\nPipeline complete!")
print(f"Converted audio saved at: {converted_audio}")
print(f"Separated stems saved in: {spleeter_output if spleeter_output else 'Skipped'}")
print(f"Magenta output directory: {output_subdir}")
print(f"Sheets saved at: {output_pdf}")
