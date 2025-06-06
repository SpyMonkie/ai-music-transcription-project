import os

model_dir = r"D:\datasets\maestro_checkpoint\guitar2"

command = (
    f"python magenta/magenta/models/onsets_frames_transcription/onsets_frames_transcription_train.py "
    f"--examples_path=tfrecord/train.tfrecord-00000-of-00001 "
    f"--model_dir={model_dir} "
    # f"--checkpoint_file={model_dir}\\model.ckpt "
    f"--config=onsets_frames "
    f"--mode=train "
    f"--hparams=\"batch_size=1\""
)

os.system(command)
