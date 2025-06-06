import tensorflow.compat.v1 as tf
import librosa
import numpy as np
from magenta.models.onsets_frames_transcription import configs
from magenta.models.onsets_frames_transcription import train_util
from note_seq.protobuf import music_pb2
from note_seq import sequence_proto_to_midi_file, plot_sequence

# Disable TensorFlow 2.x behavior (Magenta is based on TensorFlow 1.x APIs)
tf.disable_v2_behavior()

# Load the model configuration and checkpoint
config = configs.CONFIG_MAP['onsets_frames']
hparams = config.hparams
hparams.use_cudnn = True  # Set this to False if running on CPU
hparams.batch_size = 1
checkpoint_dir = 'C:\\Users\\Christopher Wu\\seniorproj\\maestro_checkpoint\\train'  # Path to pretrained checkpoint

# Load and preprocess the audio file
audio_file = 'audio/140_Piano_VKeys_07_268_1.wav'
sample_rate = 16000
wav_data, _ = librosa.load(audio_file, sr=sample_rate, mono=True)  # Load audio as mono

# Convert the audio to a Mel spectrogram
def audio_to_input(wav_data, sample_rate):
    """Preprocess audio into a Mel spectrogram for input to the model."""
    mel_spec = librosa.feature.melspectrogram(
        y=wav_data,
        sr=sample_rate,
        n_fft=2048,
        hop_length=512,
        n_mels=229
    )
    # Normalize the spectrogram (convert to log scale)
    mel_spec = np.log1p(mel_spec).T
    return mel_spec

mel_spec = audio_to_input(wav_data, sample_rate)

# Define the TensorFlow Estimator for the transcription model
estimator = train_util.create_estimator(
    model_fn=config.model_fn,
    model_dir=checkpoint_dir,
    hparams=hparams,
)

# Define input function for the model
def input_fn(params):
    """Create an input function for the TensorFlow Estimator."""
    batch_size = params.batch_size  # Access batch_size directly from the HParams object
    # Create a dataset with the correct structure
    dataset = tf.data.Dataset.from_tensors({
        'spec': tf.convert_to_tensor(mel_spec, dtype=tf.float32),
        'length': tf.constant(mel_spec.shape[0], dtype=tf.int32),  # Add length feature
    })
    dataset = dataset.repeat(batch_size)  # Repeat for the batch size
    dataset = dataset.batch(batch_size)  # Batch the dataset
    return dataset

# Perform transcription using the model
predictions = estimator.predict(
    input_fn=lambda: input_fn(hparams),  # Pass hparams directly to input_fn
    yield_single_examples=False
)

# Extract predictions and convert to NoteSequence
for prediction in predictions:
    sequence_prediction = music_pb2.NoteSequence.FromString(
        prediction['sequence_predictions'][0]
    )
    break  # Process only the first prediction

# Save the transcription as a MIDI file
output_midi = 'transcribed_piano.mid'
sequence_proto_to_midi_file(sequence_prediction, output_midi)
plot_sequence(sequence_prediction)

print(f"Transcription complete. MIDI file saved to {output_midi}")