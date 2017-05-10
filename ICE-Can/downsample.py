#!/usr/bin/env python
from pydub import AudioSegment
import os
import sys

wav_dir = sys.argv[1]
output_dir = sys.argv[2]

for file in os.listdir(wav_dir):
	if file[-4:] == ".wav":
		print "Downsampling " + " to 44.1kHz..."
		filePath = wav_dir + "/" + file
		exportPath = output_dir + "/" + file
		try:
			sound = AudioSegment.from_file(filePath, format="wav")
		except:
			print file + " could not be downsampled."
			continue
		sound.frame_rate = 44100
		sound.export(exportPath, format="wav")
