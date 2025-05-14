import os
from music21 import converter, instrument, note, chord, stream

def transcribe_piano(audio_path, model_dir, output_dir):
    command = f"""
    onsets_frames_transcription_transcribe \
        --model_dir={model_dir} \
        --audio_path={audio_path} \
        --output_dir={output_dir} \
        --save_audio
    """

    midi_file = os.path.join(output_dir, 'transcribed_output.mid')
    stream = converter.parse(midi_file)
    stream.show('musicxml')

    audio_path = 'transcribed_output.wav'
    model_dir = 'maestro_checkpoint/train/'