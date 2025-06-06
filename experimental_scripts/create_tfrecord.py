import os

# === CONFIG ===
MAGENTA_SCRIPT = "magenta/magenta/models/onsets_frames_transcription/onsets_frames_transcription_create_tfrecords.py"
CSV_PATH = "file_list.csv"
OUTPUT_DIR = "tfrecord/"
WAV_DIR = "D:/datasets/converted_wavs"
MIDI_DIR = "D:/datasets/midi"
EXPECTED_SPLITS = "train"  # Or use "train,validation,test" if you're labeling that way
NUM_SHARDS = "0"  # 0 means auto-shard based on size
# ===============

# Build the command
create_dataset_cmd = (
    f"python {MAGENTA_SCRIPT} "
    f"--csv=\"{CSV_PATH}\" "
    f"--output_directory=\"{OUTPUT_DIR}\" "
    f"--num_shards={NUM_SHARDS} "
    f"--wav_dir=\"{WAV_DIR}\" "
    f"--midi_dir=\"{MIDI_DIR}\" "
    f"--expected_splits={EXPECTED_SPLITS}"
)

# Run the command
print("Running TFRecord creation...")
os.system(create_dataset_cmd)
print("✅ Dataset TFRecord files created successfully!")
