import os
import sys

# requires ffmpeg which I installed using choco; chocolatey wasn't on path
sys.path.append('C:/ProgramData/chocolatey/bin/') 

# change cwd 
os.chdir("YOUR PATH")

# import converter
from pydub import AudioSegment

# assign file and new filename
m4a_file= "test.m4a"
wav_filename = "test.wav"

# convert m4a to wav
sound = AudioSegment.from_file(m4a_file, format = 'm4a')
file_handle = sound.export(wav_filename, format = 'wav')
