import os
import numpy as np
import tensorflow as tf
import librosa

# Define necessary functions (load, extract mel spectrogram, pad spectrogram, etc.)
def load_model(model_path="cnn_model-best.h5"):
    loaded_model = tf.keras.models.load_model(model_path)
    print(f"Model loaded from: {model_path}")
    return loaded_model

def extract_mel_spectrogram(audio_file, n_mels=128, n_fft=2048, hop_length=512):
    y, sr = librosa.load(audio_file, sr=None)
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, n_fft=n_fft, hop_length=hop_length)
    log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
    return log_spectrogram

def pad_spectrogram(spec, max_len=128):
    if spec.shape[1] < max_len:
        pad_width = max_len - spec.shape[1]
        spec = np.pad(spec, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        spec = spec[:, :max_len]
    return spec

def predict_confidence(model, audio_file, max_pad_len=128):
    spectrogram = extract_mel_spectrogram(audio_file)
    spectrogram = pad_spectrogram(spectrogram, max_pad_len)
    spectrogram = np.expand_dims(spectrogram, axis=-1)  # Add channel dimension
    spectrogram = np.expand_dims(spectrogram, axis=0)    # Add batch dimension

    prediction = model.predict(spectrogram)
    predicted_class = np.argmax(prediction, axis=1)[0]  # 0 = Doubtful, 1 = Confident

    if predicted_class == 1:
        return "Confident"
    else:
        return "Doubtful"

# Example usage
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
audio_file = 'speech_recognition/microphone-results.wav'  # Provide path to new audio file
loaded_model = load_model("cnn_model-best.h5")
confidence_level = predict_confidence(loaded_model, audio_file)
print(f"The input file is classified as: {confidence_level}")