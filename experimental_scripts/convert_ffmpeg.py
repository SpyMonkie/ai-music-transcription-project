import os
import subprocess

def convert_wav_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    wav_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".wav")]
    print(f"Found {len(wav_files)} .wav files in {input_dir}")

    for filename in wav_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # ffmpeg command to convert to 16kHz mono WAV
        command = f'ffmpeg -y -i "{input_path}" -ar 16000 -ac 1 "{output_path}"'
        print(f"Converting: {filename}")
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print(f"❌ Error converting {filename}")
            print(result.stderr.decode())
        else:
            print(f"✅ Saved: {output_path}")

    print("\nAll conversions done.")

# Example usage:
input_directory = r"D:\datasets\audio_hex-pickup_original"
output_directory = r"D:\datasets\converted_wavs"

convert_wav_directory(input_directory, output_directory)
