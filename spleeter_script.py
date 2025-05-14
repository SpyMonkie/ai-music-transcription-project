import os
import subprocess
import sys

def run_spleeter(input_file, output_dir):
    try:
        command = [
            "spleeter",
            "separate",
            "-p", "spleeter:5stems",
            "-o", output_dir,
            input_file
        ]
        subprocess.run(command, check=True)
        print(f"Successfully processed {input_file}!")
    except subprocess.CalledProcessError as e:
        print(f"Error running Spleeter: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python spleeter_script.py <input_file> <output_directory>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    run_spleeter(input_file, output_dir)
