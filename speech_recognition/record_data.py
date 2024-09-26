import speech_recognition as sr
import wave
import os

# Define actor number
actor_number = 1  # Change this number to distinguish different actors

# Function to record and transcribe audio using the microphone
def record_and_transcribe():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Please speak now...")
        
        # Adjust for ambient noise and record audio
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio_data = recognizer.listen(source)
        print("Recording complete, processing...")
        
        try:
            # Transcribe speech to text using Google Web Speech API
            transcription = recognizer.recognize_google(audio_data)
            print(f"Transcription: {transcription}")
            return audio_data, transcription
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None, None
        except sr.RequestError as e:
            print(f"Error with Google Web API: {e}")
            return None, None

# Function to save the audio file
def save_audio(audio_data, folder_name, transcription, sample_type, actor_number):
    # Ensure folder exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Create the filename with the transcription, sample type, and actor number
    filename = f"{folder_name}/{transcription}_{sample_type}_actor{actor_number}.wav"
    
    # Save the audio as a WAV file
    with wave.open(filename, "wb") as f:
        f.setnchannels(1)  # Mono channel
        f.setsampwidth(2)  # 2 bytes per sample (16-bit)
        f.setframerate(44100)  # sample rate (44.1 kHz)
        f.writeframes(audio_data.get_wav_data())
    
    print(f"Audio saved as {filename}")

# Function to record and save confident or doubtful samples
def record_samples():
    # Prompt for 'c' for confident and 'd' for doubtful
    sample_type = input("Do you want to record a 'confident (c)' or 'doubtful (d)' response? ").strip().lower()
    
    if sample_type not in ["c", "d"]:
        print("Invalid response type. Please enter 'c' for confident or 'd' for doubtful.")
        return
    
    # Record and transcribe the user's response
    audio_data, transcription = record_and_transcribe()
    
    if transcription:
        # Set the root folder as 'recordings'
        root_folder = "recordings"
        
        # Set folder name based on sample type (confident or doubtful)
        folder_name = os.path.join(root_folder, "confident" if sample_type == "c" else "doubtful")
        
        # Save the audio file in the appropriate folder
        save_audio(audio_data, folder_name, transcription, "confident" if sample_type == "c" else "doubtful", actor_number)
    else:
        print("Skipping saving this file due to transcription failure.")

if __name__ == "__main__":
    while True:
        record_samples()  # Continuously prompt for new recordings
        # Ask 'y' for yes or 'n' for no when prompting to record another sample
        another = input("Would you like to record another sample? (y/n): ").strip().lower()
        if another != "y":
            print("Exiting...")
            break