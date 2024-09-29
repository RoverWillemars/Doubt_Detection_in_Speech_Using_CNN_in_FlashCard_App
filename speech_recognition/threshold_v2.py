import os
import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import seaborn as sns

def plot_mfcc(file):
    
    y, sr = librosa.load(file)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)

    fig, ax = plt.subplots(nrows=3, sharex=True, sharey=True)
    img1 = librosa.display.specshow(mfcc, ax=ax[0], x_axis='time')
    ax[0].set(title='MFCC')
    ax[0].label_outer()
    img2 = librosa.display.specshow(mfcc_delta, ax=ax[1], x_axis='time')
    ax[1].set(title=r'MFCC-$\Delta$')
    ax[1].label_outer()
    img3 = librosa.display.specshow(mfcc_delta2, ax=ax[2], x_axis='time')
    ax[2].set(title=r'MFCC-$\Delta^2$')
    fig.colorbar(img1, ax=[ax[0]])
    fig.colorbar(img2, ax=[ax[1]])
    fig.colorbar(img3, ax=[ax[2]])
    plt.show()


# plot f0 over time
def plot_f0(file):
    
    y, sr = librosa.load(file)
    f0, voiced_flag, voiced_probs = librosa.pyin(y,
                                                sr=sr,
                                                fmin=librosa.note_to_hz('C2'),
                                                fmax=librosa.note_to_hz('C7'))
    times = librosa.times_like(f0, sr=sr)


    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    fig, ax = plt.subplots()
    img = librosa.display.specshow(D, x_axis='time', y_axis='log', ax=ax)
    ax.set(title='pYIN fundamental frequency estimation')
    fig.colorbar(img, ax=ax, format="%+2.f dB")
    ax.plot(times, f0, label='f0', color='cyan', linewidth=3)
    ax.legend(loc='upper right')
    plt.show()


def plot_pairwise_combinations_in_grid(df, label_col='Doubt', n_cols=3):
    # get the list of numeric columns (excluding the doubt dummy)
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    # collect pairwise combinations
    #combinations = list(itertools.combinations(numeric_columns + [label_col], 2))
    combinations = list(itertools.combinations(numeric_columns, 2))

    # set the number of rows based
    n_rows = int(np.ceil(len(combinations) / n_cols))

    # create subplots grid
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 5))
    axes = axes.flatten()  # Flatten the grid of axes for easy indexing

    for i, (x_col, y_col) in enumerate(combinations):
        ax = axes[i]  # Get the current axis

        if x_col == label_col or y_col == label_col:
            # one of the variables is the dummy variable, create a boxplot
            variable_col = x_col if y_col == label_col else y_col
            sns.boxplot(x=df[label_col], y=df[variable_col], ax=ax, palette=['green', 'red'])
            ax.set_title(f'{variable_col} distribution for Confident (0) and Doubtful (1)')
            ax.set_xlabel('Doubt (0 = Confident, 1 = Doubtful)')
            ax.set_ylabel(variable_col)

        else:
            # create scatter plot for confident and doubtful
            confident_data = df[df[label_col] == 0]
            doubtful_data = df[df[label_col] == 1]

            ax.scatter(confident_data[x_col], confident_data[y_col], color='green', label='Confident', alpha=0.7)
            ax.scatter(doubtful_data[x_col], doubtful_data[y_col], color='red', label='Doubtful', alpha=0.7)

            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f'{x_col} vs {y_col}')
            ax.legend()

    # hide any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


# Function to create pairwise scatter plots for all variable combinations
def plot_pairwise_combinations(df, label_col='Doubt'):
    # Get the list of numeric columns (excluding the doubt dummy)
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    # collect pairwise combinations
    combinations = list(itertools.combinations(numeric_columns, 2))

    # Iterate over each pair of numeric columns and create a scatter plot
    for x_col, y_col in combinations:
        plt.figure(figsize=(10, 5))

        if x_col == label_col or y_col == label_col:
            # One of the variables is the dummy variable
            variable_col = x_col if y_col == label_col else y_col

            # create boxplot
            sns.boxplot(x=df[label_col], y=df[variable_col], palette=['green', 'red'])
            plt.title(f'{variable_col} distribution for Confident (0) and Doubtful (1)')
            plt.xlabel('Doubt (0 = Confident, 1 = Doubtful)')
            plt.ylabel(variable_col)

        else:
            # neither variable is the dummy, create scatter plot
            confident_data = df[df[label_col] == 0]
            doubtful_data = df[df[label_col] == 1]

            # plot confident responses (in green)
            plt.scatter(confident_data[x_col], confident_data[y_col], color='green', label='Confident', alpha=0.7)

            # plot doubtful responses (in red)
            plt.scatter(doubtful_data[x_col], doubtful_data[y_col], color='red', label='Doubtful', alpha=0.7)

            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.legend()
            plt.title(f'{x_col} vs {y_col} for Confident and Doubtful Responses')

        plt.show()

# Extract pitch and volume for a single audio file
def extract_features(audio_file):
    y, sr = librosa.load(audio_file)

    # Extract pitch (fundamental frequency)
    #f0, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    
    # Extract pitch using pyin (better for single pitch)
    f0,voiced_flag, voiced_probs = librosa.pyin(y,
                        sr=sr,
                        fmin=librosa.note_to_hz('C2'),
                        fmax=librosa.note_to_hz('C7')) 

    # Extract volume (RMS energy)
    rms = librosa.feature.rms(y=y)[0]

    # calculate mean and deviation from pitch
    f0_mean = np.nanmean(f0)
    f0_sd = np.nanstd(f0)
    f0_CoV = f0_sd / f0_mean
    
    # calculate mean and deviation from volume
    volume_mean = np.mean(rms)
    volume_sd = np.nanstd(rms)
    volume_CoV = volume_sd /volume_mean
    
    # calculate jitter
    jitter = np.mean(np.abs(np.diff(f0[f0 > 0])))
    jitter_percentage = (jitter / np.mean(f0[f0 > 0])) * 100 # jitter values above 1% typically indicate instability

    return f0_mean, volume_mean, f0_CoV, volume_CoV, jitter_percentage

# Collect features for multiple audio files (confident and doubtful)
def collect_features(audio_files, doubt_dummy):
    data = []

    for audio_file in audio_files:
        pitch, volume, f0_CoV, volume_CoV, jitter = extract_features(audio_file)
        data.append({
            "Filename": os.path.basename(audio_file),
            "Doubt": doubt_dummy,  # confident (1) or doubtful (0)
            "Pitch_Mean": pitch,
            "Volume_Mean": volume,
            "Pitch_CoV": f0_CoV,
            "Volume_CoV": volume_CoV,
            "Jitter_Perc": jitter
        })

    return pd.DataFrame(data)

# Function to get all audio files rated and stored in excel file
def get_audio_files_from_directory(directory, file_list):
    audio_files = []
    for path, subdirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename in file_list: # edit
                audio_files.append(os.path.join(path, filename))
    return audio_files

# specify path
os.chdir("C:/users/remon/OneDrive/Bureaublad/BCN_ReMa2/User_Modelling/speech_data")
dir = os.getcwd()

# read excel sheet
df = pd.read_excel('rating.xlsx')
df = df.iloc[:,0:2].dropna()
confidence_list = df.loc[df["doubt (0-1)"] == 0, "filename"].tolist()
doubtful_list = df.loc[df["doubt (0-1)"] == 1, "filename"].tolist()

# Get all audio files from the directories
confident_files = get_audio_files_from_directory(dir, confidence_list)
doubtful_files = get_audio_files_from_directory(dir, doubtful_list)

# Collect features for confident and doubtful responses
confident_df = collect_features(confident_files, 0)
doubtful_df = collect_features(doubtful_files, 1)

# concatenate
both_df = pd.concat([confident_df, doubtful_df])

# plot
plot_pairwise_combinations(both_df, "Doubt")
plot_pairwise_combinations_in_grid(both_df, "Doubt", 3)
