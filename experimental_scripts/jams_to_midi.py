from GuitarSet.visualize.interpreter import jams_to_midi
import os
import glob
import jams

# Change these paths to match your dataset
INPUT_DIR = 'D:\\datasets\\annotation'
OUTPUT_DIR = 'D:\\datasets\\midi'

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Loop through all .jams files in the input directory
jams_files = glob.glob(os.path.join(INPUT_DIR, '*.jams'))
print(f"Found {len(jams_files)} .jams files.")

for jams_path in jams_files:
    try:
        # Load the .jams file
        jam = jams.load(jams_path)

        # Convert to MIDI
        midi = jams_to_midi(jam)

        # Get output filename
        filename = os.path.basename(jams_path).replace('.jams', '.mid')
        output_path = os.path.join(OUTPUT_DIR, filename)

        # Write to disk
        midi.write(output_path)
        print(f"✅ Converted: {filename}")

    except Exception as e:
        print(f"❌ Failed to convert {jams_path}: {e}")