import os
import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Extract pitch and volume for a single audio file
def extract_features(audio_file):
    y, sr = librosa.load(audio_file)

    # Extract pitch (fundamental frequency)
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

    # Extract volume (RMS energy)
    rms = librosa.feature.rms(y=y)[0]

    # Calculate mean pitch and volume
    mean_pitch = np.mean(pitches[pitches > 0])  # Avoid zero-pitch values
    mean_volume = np.mean(rms)

    return mean_pitch, mean_volume

# Collect features for multiple audio files (confident and doubtful)
def collect_features(audio_files):
    pitch_values = []
    volume_values = []

    for audio_file in audio_files:
        pitch, volume = extract_features(audio_file)
        pitch_values.append(pitch)
        volume_values.append(volume)

    return pitch_values, volume_values

# Function to get all audio files rated and stored in excel file
def get_audio_files_from_directory(directory, file_list):
    audio_files = []
    for path, subdirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename in file_list: # edit
                audio_files.append(os.path.join(path, filename))
    return audio_files

# specify path
os.chdir("YOUR PATH")
dir = os.getcwd()

# read excel sheet
df = pd.read_excel('rateing.xlsx')
df = df.iloc[:,0:2].dropna()
confidence_list = df.loc[df["doubt (0-1)"] == 0, "filename"].tolist()
doubtful_list = df.loc[df["doubt (0-1)"] == 1, "filename"].tolist()

# Get all audio files from the directories
confident_files = get_audio_files_from_directory(dir, confidence_list)
doubtful_files = get_audio_files_from_directory(dir, doubtful_list)

# Collect features for confident and doubtful responses
confident_pitch, confident_volume = collect_features(confident_files)
doubtful_pitch, doubtful_volume = collect_features(doubtful_files)

# Step 3: Visualize the data using a scatter plot
plt.figure(figsize=(10, 5))

# Plot confident responses (in green)
plt.scatter(confident_pitch, confident_volume, color='green', label='Confident', alpha=0.7)

# Plot doubtful responses (in red)
plt.scatter(doubtful_pitch, doubtful_volume, color='red', label='Doubtful', alpha=0.7)

plt.xlabel('Pitch (Mean Fundamental Frequency)')
plt.ylabel('Volume (Mean RMS)')
plt.legend()
plt.title('Pitch vs. Volume for Confident and Doubtful Responses')
plt.show()

# Calculate mean values for confident and doubtful samples
mean_confident_pitch = np.mean(confident_pitch)
mean_confident_volume = np.mean(confident_volume)
mean_doubtful_pitch = np.mean(doubtful_pitch)
mean_doubtful_volume = np.mean(doubtful_volume)

# Set thresholds as the midpoint between confident and doubtful averages
threshold_pitch = (mean_confident_pitch + mean_doubtful_pitch) / 2
threshold_volume = (mean_confident_volume + mean_doubtful_volume) / 2

print(f"Threshold Pitch: {threshold_pitch}")
print(f"Threshold Volume: {threshold_volume}")
