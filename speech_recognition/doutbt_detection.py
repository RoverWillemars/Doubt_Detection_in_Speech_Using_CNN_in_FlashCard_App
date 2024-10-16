import os
import speech_recognition as sr
import librosa
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Step 1: Convert audio to text using SpeechRecognition
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

# Step 2: Extract acoustic features using librosa
def extract_audio_features(audio_file):
    y, sr = librosa.load(audio_file)

    # Extract pitch (fundamental frequency)
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

    # Extract volume (Root Mean Square Energy)
    rms = librosa.feature.rms(y=y)[0]

    # Calculate speech rate (how many words per second)
    duration = librosa.get_duration(y=y, sr=sr)

    # Return feature statistics
    return {
        'mean_pitch': np.mean(pitches[pitches > 0]),  # Avoid zero-pitch values
        'mean_volume': np.mean(rms),
        'speech_duration': duration
    }

# Step 3: Prepare dataset for training
def prepare_dataset(confident_dir, doubtful_dir):
    features = []
    labels = []

    # Process confident files
    for filename in os.listdir(confident_dir):
        if filename.endswith('.wav'):
            file_path = os.path.join(confident_dir, filename)
            feature = extract_audio_features(file_path)
            features.append([feature['mean_pitch'], feature['mean_volume'], feature['speech_duration']])
            labels.append(1)  # 1 for confident

    # Process doubtful files
    for filename in os.listdir(doubtful_dir):
        if filename.endswith('.wav'):
            file_path = os.path.join(doubtful_dir, filename)
            feature = extract_audio_features(file_path)
            features.append([feature['mean_pitch'], feature['mean_volume'], feature['speech_duration']])
            labels.append(0)  # 0 for doubtful

    return np.array(features), np.array(labels)

# Step 4: Train the SVM model
def train_svm_model(features, labels):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    clf = svm.SVC(kernel='linear')  # You can also experiment with other kernels
    clf.fit(X_train, y_train)

    # Evaluate the model
    predictions = clf.predict(X_test)
    print(classification_report(y_test, predictions, target_names=["Doubtful", "Confident"]))
    
    return clf

# Step 5: Analyze for confidence using the trained model
def analyze_confidence(model, audio_file):
    features = extract_audio_features(audio_file)
    sample_features = np.array([[features['mean_pitch'], features['mean_volume'], features['speech_duration']]])
    
    prediction = model.predict(sample_features)
    
    return "Confident" if prediction[0] == 1 else "Doubtful"

if __name__ == "__main__":
    # Directory paths
    confident_dir = 'speech_recognition/Data/confident/'
    doubtful_dir = 'speech_recognition/Data/doubtful/'

    # Prepare dataset and train SVM model
    features, labels = prepare_dataset(confident_dir, doubtful_dir)
    svm_model = train_svm_model(features, labels)

    # output explanation:
    # Precision Definition: The ratio of true positive predictions to the total positive predictions made by the model. It indicates how many of the predicted positive cases (e.g., "Confident") were actually correct. Interpretation: A higher precision means that when the model predicts "Confident," it is more likely to be correct.
    # Recall Definition: The ratio of true positive predictions to the total actual positives in the dataset. It indicates how many of the actual positive cases were correctly identified by the model. Interpretation: A higher recall means that the model successfully identifies most of the true "Confident" cases.
    # F1-Score Definition: The harmonic mean of precision and recall. It provides a single score that balances both the concerns of precision and recall. Interpretation: A higher F1-score indicates a better balance between precision and recall.
    # Support Definition: The number of actual occurrences of each class in the specified dataset. Interpretation: This helps you understand how many examples of each class the model was trained and tested on.
    # Accuracy: The overall accuracy of the model is 0.86, meaning it correctly classified 86% of the total test samples.
    # Macro Avg: These values represent the average performance across both classes without considering the support. They give an overall view of the model's performance.
    # Weighted Avg: This is similar to the macro average but considers the number of instances for each class, giving a more nuanced view of performance, especially useful when dealing with imbalanced datasets.

    # Example usage
    audio_file = 'speech_recognition/recordings/confident/Afghanistan_confident_actor1.wav'  # Replace with the path to your audio file
    confidence_level = analyze_confidence(svm_model, audio_file)
    print(f"The response is: {confidence_level}")