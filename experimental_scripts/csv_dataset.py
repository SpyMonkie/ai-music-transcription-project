# import os
# import csv

# # ==== CONFIG ====
# # Set your directory path here
# DATASET_DIR = 'D:/datasets/audio_hex-pickup_original'  # Example path
# OUTPUT_FILE = 'file_list.csv'  # Can also be 'file_list.txt'
# FILE_EXT = '.wav'  # Or '.mid' or any extension you need
# # ================

# # Get all files with the desired extension
# file_list = [f for f in os.listdir(DATASET_DIR) if f.lower().endswith(FILE_EXT)]

# # Sort for consistency
# file_list.sort()

# # Write to CSV
# with open(OUTPUT_FILE, 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['filename'])  # Header
#     for filename in file_list:
#         writer.writerow([filename])

# print(f"✅ Wrote {len(file_list)} filenames to {OUTPUT_FILE}")


import os
import csv

# ==== CONFIG ====
WAV_DIR = 'D:/datasets/audio_hex-pickup_original'
MIDI_DIR = 'D:/datasets/midi'
OUTPUT_FILE = 'file_list.csv'
WAV_EXT = '.wav'
MIDI_EXT = '.mid'
SPLIT_LABEL = 'train'  # You can change this to 'train' or 'val' as needed
# ================

# List and sort files
wav_files = sorted([f for f in os.listdir(WAV_DIR) if f.lower().endswith(WAV_EXT)])
midi_files = sorted([f for f in os.listdir(MIDI_DIR) if f.lower().endswith(MIDI_EXT)])



# Write to CSV
with open(OUTPUT_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['audio_filename', 'midi_filename', 'split'])  # CSV header
    for i in range(len(wav_files)):
        writer.writerow([wav_files[i], midi_files[i], SPLIT_LABEL])

print(f"✅ Wrote {len(wav_files)} matched rows with label '{SPLIT_LABEL}' to {OUTPUT_FILE}")
