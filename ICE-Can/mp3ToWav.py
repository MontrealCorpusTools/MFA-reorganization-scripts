#!/usr/bin/env python
from pydub import AudioSegment
import os
import sys

mp3_dir = sys.argv[1]

for file in os.listdir(mp3_dir):
	if file[-4:] == ".mp3":
		print "Converting " + file + "from .mp3 to .wav..."
		fileName = file.split(".")
		exportName = fileName[0] + ".wav"
		filePath = mp3_dir + "/" + file
		sound = AudioSegment.from_mp3(filePath)
		sound.export(exportName, format="wav")