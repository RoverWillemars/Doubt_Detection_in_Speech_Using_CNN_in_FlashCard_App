## first attempt at speech recognition. Works quite okay. 
## For now I only tried Google Speech Recognition here, as it doesn't require any API key.

import os
import speech_recognition as sr

# set cwd
os.chdir("YOUR_DIR")

# assign file
filename = "test.wav"

# initialize Google Speech Recognition --> I need to play around with this a little more.
r = sr.Recognizer()

# open the file
with sr.AudioFile(filename) as source:

    # load audio to memory
    audio_data = r.record(source)

    # convert speech to text
    text = r.recognize_google(audio_data)
    print(text)
