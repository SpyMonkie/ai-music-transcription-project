import tensorflow as tf
import magenta
import librosa
import note_seq

print("TensorFlow version:", tf.__version__)
print("Magenta version:", magenta.__version__)
print("Librosa version:", librosa.__version__)
print("Note-seq version:", note_seq.__version__)
print("Num of GPUs Available:", len(tf.config.experimental.list_physical_devices('GPU')))

print(tf.sysconfig.get_build_info())