import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import subprocess
import os
import shutil
import threading
import pretty_midi

progress_popup = None

def quantize_midi(input_path, output_path, resolution=0.05, min_duration=0.05):
    midi = pretty_midi.PrettyMIDI(input_path)
    for instrument in midi.instruments:
        for note in instrument.notes:
            note.start = round(note.start / resolution) * resolution
            note.end = round(note.end / resolution) * resolution
            if note.end <= note.start:
                note.end = note.start + min_duration
    midi.write(output_path)

def show_progress(message):
    # status_label.config(text=message)
    # status_label.pack(pady=(10, 0))
    # progress.pack(pady=(0, 10))
    # progress.start()
    global progress_popup
    progress_popup = tk.Toplevel(root)
    progress_popup.title("Please Wait")
    progress_popup.geometry("300x100")
    progress_popup.resizable(False, False)

    label = tk.Label(progress_popup, text=message, font=("Arial", 12))
    label.pack(pady=20)

    pb = ttk.Progressbar(progress_popup, orient="horizontal", mode="indeterminate", length=200)
    pb.pack(pady=10)
    pb.start()

    progress_popup.transient(root)
    progress_popup.grab_set()  # Make the popup modal

def hide_progress(done_message):
    # progress.stop()
    # progress.pack_forget()
    # status_label.config(text=done_message)
    global progress_popup
    if progress_popup:
        progress_popup.destroy()
        progress_popup = None

def convert_audio():
    if not input_audio.get():
        messagebox.showerror("Missing Input", "Please select an input audio file.")
        return

    out_wav = filedialog.asksaveasfilename(defaultextension=".wav", title="Save Converted WAV File")
    if not out_wav:
        return

    show_progress("Converting audio to 16kHz WAV...")

    def convert_task():
        cmd = f'ffmpeg -i "{input_audio.get()}" -ar 16000 -ac 1 "{out_wav}"'
        os.system(cmd)
        converted_audio.set(out_wav)
        hide_progress("Conversion complete.")
        messagebox.showinfo("Success", f"Audio converted and saved to:\n{out_wav}")

    threading.Thread(target=convert_task).start()

def run_spleeter():
    # if not converted_audio.get():
    #     messagebox.showerror("Missing File", "Convert or select an audio file first.")
    #     return

    if not converted_audio.get():
        messagebox.showinfo("No File Selected", "Please select a converted audio file.")
        selected_file = filedialog.askopenfilename(title="Select Converted Audio File")
        if not selected_file:
            return
        converted_audio.set(selected_file)

    out_dir = filedialog.askdirectory(title="Select Folder to Save Separated Stems")
    if not out_dir:
        return

    show_progress("Separating stems with Spleeter...")

    def spleeter_task():
        cmd = f'spleeter separate -p spleeter:5stems -o "{out_dir}" "{converted_audio.get()}"'
        os.system(cmd)
        hide_progress("Stems separated successfully.")
        spleeter_output.set(out_dir)
        messagebox.showinfo("Done", f"Stems saved to:\n{out_dir}")

    threading.Thread(target=spleeter_task).start()

    # cmd = f'spleeter separate -p spleeter:5stems -o "{out_dir}" "{converted_audio.get()}"'
    # os.system(cmd)
    # spleeter_output.set(out_dir)
    # messagebox.showinfo("Done", f"Stems saved to:\n{out_dir}")

def run_magenta():
    # if not spleeter_output.get():
    #     messagebox.showerror("Missing Stems", "Please run Spleeter first.")
    #     return

    stem_file = filedialog.askopenfilename(title="Select Stem to Transcribe (e.g. piano.wav or drums.wav)")
    if not stem_file:
        return

    if not stem_file.endswith('.wav'):
        messagebox.showerror("Invalid File", "Please select a valid WAV file.")
        return

    out_dir = filedialog.askdirectory(title="Select Output Directory for MIDI")
    if not out_dir:
        return

    song_name_dir = simpledialog.askstring("Input", "Enter a name for the new directory:")
    if song_name_dir is None or song_name_dir.strip() == "":
        messagebox.showerror("Invalid Name", "Please enter a valid song name.")
        return

    show_progress("Running Magenta transcription...")

    def magenta_task():
        try:
            model_type = model_choice.get()
            model_dir = "./maestro_checkpoint/piano" if model_type == "Piano" else "./maestro_checkpoint/drum"
            config = "onsets_frames" if model_type == "Piano" else "drums"

            # 1. Create a subdirectory for the output
            # song_name_dir = os.path.splitext(os.path.basename(stem_file))[0]


            output_subdir = os.path.join(out_dir, song_name_dir.strip())
            os.makedirs(output_subdir, exist_ok=True)

            # 2. Copy the stem file to the output directory
            local_stem_path = os.path.join(output_subdir, os.path.basename(stem_file))
            shutil.copy(stem_file, local_stem_path)

            # 3. Run Magenta transcription
            # original_dir = os.getcwd()
            # os.chdir(output_subdir)

            # 4. Run the Magenta transcription command
            cmd = (
                f"python magenta/magenta/models/onsets_frames_transcription/onsets_frames_transcription_transcribe.py "
                f"--config={config} --model_dir={model_dir} \"{local_stem_path}\""
            )
            os.system(cmd)

            # 5. Restore the original directory
            # os.chdir(original_dir)

            hide_progress("Transcription complete.")
            messagebox.showinfo("Done", "Transcription complete.")
        except Exception as e:
            hide_progress("Error during transcription.")
            print(f"Error: {e}")
            messagebox.showerror("Error", "Magenta failed to transcribe the file.")

    threading.Thread(target=magenta_task).start()

def midi_to_pdf():
    midi_file = filedialog.askopenfilename(title="Select MIDI File")
    if not midi_file:
        return

    out_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save PDF")
    if not out_pdf:
        return

    show_progress("Quantizing MIDI and converting to PDF...")

    def midi_to_pdf_task():

        try:
            # Construct quantized file path
            midi_dir = os.path.dirname(midi_file)
            midi_base = os.path.basename(midi_file)
            quantized_path = os.path.join(midi_dir, f"quantized_{midi_base}")

            # Quantize the MIDI file
            quantize_midi(midi_file, quantized_path)

            cmd = ["musescore4", quantized_path, "-o", out_pdf]
            subprocess.run(cmd, check=True)
            hide_progress("PDF conversion complete.")
            messagebox.showinfo("Success", f"PDF saved to:\n{out_pdf}")
        except subprocess.CalledProcessError:
            hide_progress("Error during conversion.")
            messagebox.showerror("Error", "MuseScore failed to convert the file.")

    threading.Thread(target=midi_to_pdf_task).start()


root = tk.Tk()
root.title("Music Transcription Pipeline")
root.geometry("800x600")

input_audio = tk.StringVar()
converted_audio = tk.StringVar()
spleeter_output = tk.StringVar()
model_choice = tk.StringVar(value="Piano")
# status_label = tk.Label(root, text="", font=("Arial", 10))
# progress = ttk.Progressbar(root, orient="horizontal", mode="indeterminate", length=300)


# File selection
tk.Label(root, text="Input Audio File:").pack(anchor='w', padx=10)
tk.Entry(root, textvariable=input_audio, width=60).pack(padx=10)
tk.Button(root, text="Browse", command=lambda: input_audio.set(filedialog.askopenfilename())).pack(padx=10, pady=5)

# Buttons for each step
tk.Button(root, text="1. Convert Audio to 16kHz WAV", command=convert_audio).pack(pady=5)
tk.Button(root, text="2. Separate Stems with Spleeter", command=run_spleeter).pack(pady=5)

# Model selection
tk.Label(root, text="3. Choose Transcription Model:").pack()
ttk.Combobox(root, textvariable=model_choice, values=["Piano", "Drums"]).pack(pady=2)
tk.Button(root, text="4. Run Magenta Transcription", command=run_magenta).pack(pady=5)

# Convert MIDI to PDF
tk.Button(root, text="5. Convert MIDI to Sheet Music PDF", command=midi_to_pdf).pack(pady=10)

instructions = (
    "This tool allows you to:\n"
    "- Convert audio to 16kHz mono WAV\n"
    "- Separate stems using Spleeter\n"
    "- Transcribe piano or drums using Magenta\n"
    "- Convert MIDI files to clean PDF sheet music\n\n"
    "Each step is independent — you can run them in any order.\n\n"
    "Requirements:\n"
    "- MuseScore 4 for PDF export\n"
    "- ffmpeg, spleeter, and Magenta installed\n"
)
tk.Label(root, text=instructions, justify='left', wraplength=560, font=("Arial", 10)).pack(padx=20, pady=10)

root.mainloop()
