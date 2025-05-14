import os

magenta_command = (
    "python magenta/magenta/models/onsets_frames_transcription/onsets_frames_transcription_transcribe.py "
    "--config=onsets_frames "
    "--model_dir=./maestro_checkpoint/guitar "
    "./audio/relaxing_guitar.wav "
)

os.system(magenta_command)

# os.system(command)
