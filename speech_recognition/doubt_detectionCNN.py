import os
import librosa
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt

# Step 1: Extract Mel Spectrograms
def extract_mel_spectrogram(audio_file, n_mels=128, n_fft=2048, hop_length=512):
    y, sr = librosa.load(audio_file, sr=None)
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, n_fft=n_fft, hop_length=hop_length)
    log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
    return log_spectrogram

# Define pad_spectrogram to pad spectrograms to a consistent length
def pad_spectrogram(spec, max_len=128):
    if spec.shape[1] < max_len:
        pad_width = max_len - spec.shape[1]
        spec = np.pad(spec, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        spec = spec[:, :max_len]
    return spec

# Step 2: Prepare the dataset
def prepare_dataset(confident_dir, doubtful_dir, max_pad_len=128):
    spectrograms = []
    labels = []

    # Process confident files
    for filename in os.listdir(confident_dir):
        if filename.endswith('.wav'):
            file_path = os.path.join(confident_dir, filename)
            spectrogram = extract_mel_spectrogram(file_path)
            spectrogram = pad_spectrogram(spectrogram, max_pad_len)
            spectrograms.append(spectrogram)
            labels.append(1)  # 1 for confident

    # Process doubtful files
    for filename in os.listdir(doubtful_dir):
        if filename.endswith('.wav'):
            file_path = os.path.join(doubtful_dir, filename)
            spectrogram = extract_mel_spectrogram(file_path)
            spectrogram = pad_spectrogram(spectrogram, max_pad_len)
            spectrograms.append(spectrogram)
            labels.append(0)  # 0 for doubtful

    spectrograms = np.array(spectrograms)
    labels = np.array(labels)

    # Reshape the spectrograms for CNN input (Add channel dimension)
    spectrograms = spectrograms[..., np.newaxis]

    return spectrograms, labels

# Step 3: Define the CNN model
def create_cnn_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(2, activation='softmax')  # Two classes: Confident and Doubtful
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Step 4: Train the CNN model
def train_cnn_model(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32):
    history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size)
    return history

# Step 5: Save the trained model
def save_model(model, model_path="cnn_model.h5"):
    model.save(model_path)
    print(f"Model saved at: {model_path}")

# Step 6: Load a pre-trained model
def load_model(model_path="cnn_model.h5"):
    loaded_model = tf.keras.models.load_model(model_path)
    print(f"Model loaded from: {model_path}")
    return loaded_model

# Step 7: Fine-tune the loaded model on new data
def fine_tune_model(model, X_train, y_train, X_val, y_val, fine_tune_epochs=10, fine_tune_lr=1e-5):
    # Compile the model with a lower learning rate
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=fine_tune_lr),
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    # Fine-tune the model
    history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=fine_tune_epochs)
    return history

# Step 8: Evaluate model on the validation data
def evaluate_model(model, X_val, y_val):
    predictions = model.predict(X_val)
    predicted_classes = np.argmax(predictions, axis=1)

    # Confusion matrix and classification report
    cm = confusion_matrix(y_val, predicted_classes)
    cr = classification_report(y_val, predicted_classes, target_names=['Doubtful', 'Confident'])

    print("Confusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(cr)

    correct_confident = cm[1, 1]  # True positives (confident correctly classified)
    correct_doubtful = cm[0, 0]  # True negatives (doubtful correctly classified)

    print(f"\nCorrectly classified Confident samples: {correct_confident}")
    print(f"Correctly classified Doubtful samples: {correct_doubtful}")

# Example usage
if __name__ == "__main__":
    # Directory paths
    confident_dir = 'speech_recognition/Data/confident/'
    doubtful_dir = 'speech_recognition/Data/doubtful/'

    # Prepare dataset
    X, y = prepare_dataset(confident_dir, doubtful_dir)

    # Split dataset into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define input shape (based on mel spectrogram dimensions)
    input_shape = X_train.shape[1:]  # (n_mels, max_pad_len, 1)

    # Step 1: Train and save the CNN model
    cnn_model = create_cnn_model(input_shape)
    history = train_cnn_model(cnn_model, X_train, y_train, X_val, y_val)
    save_model(cnn_model, "cnn_model.h5")

    # Step 2: Load the saved model and fine-tune it on a smaller dataset
    loaded_model = load_model("cnn_model.h5")
    evaluate_model(loaded_model, X_val, y_val)

    confident_dir_finetune = 'speech_recognition/Recordings/confident/'
    doubtful_dir_finetune = 'speech_recognition/Recordings/doubtful/'
    X_fine, y_fine = prepare_dataset(confident_dir_finetune, doubtful_dir_finetune)
    
    # Fine-tune on a smaller set of data (this could be a new dataset or a subset of the original)
    X_train_fine, X_val_fine, y_train_fine, y_val_fine = train_test_split(X_fine, y_fine, test_size=0.2)  # Example small set
    fine_tune_history = fine_tune_model(loaded_model, X_train_fine, y_train_fine, X_val_fine, y_val_fine, fine_tune_epochs=10)
    
    # Evaluate the fine-tuned model
    evaluate_model(loaded_model, X_val_fine, y_val_fine)