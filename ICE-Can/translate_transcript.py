#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ICE copy
import os
import re
import wave
import contextlib
import xlrd
from scipy.io import wavfile
from textgrid import TextGrid, IntervalTier
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Note: ICE corpus files will sometimes produce the following warning:
	# WavFileWarning: Chunk (non-data) not understood, skipping it.
# This seems to do with some chunk in the wavs themselves and should not cause problems for the code.

# <$A>, <$B> etc. - Speaker identification
# <I>...</I> - Subtext marker
# <#> - Text unit marker
# <O>...</O> - Untranscribed text
# <?>...</?> - Uncertain transcription
# <.>...</.> - Incomplete word(s)
# <[>...</[> - Overlapping string
# <{>...</{> - Overlapping string set
# <,> - Short pause
# <,,> - Long pause
# <X>...</X> - Extra-corpus text
# <&>...</&> - Editorial comment
# <@>...</@> - Changed name or word
# <quote>...</quote> - Quotation
# <mention>...</mention> - Mention
# <foreign>...</foreign> - Foreign word(s)
# <indig>...</indig> - Indigenous word(s)
# <unclear>...</unclear> - Unclear word(s)

# All tags must eventually be deleted.
# Tags whose contents <tag>content</tag> must be kept:
	# uncertain transcription, incomplete word(s), overlapping string,
	# overlapping string set, quote, mention, subtext marker
# Other tags' contents are deleted when applicable.

transcription_text_source = sys.argv[1]
transcription_wav_source = sys.argv[2]
transcription_output = sys.argv[3]
metadata = sys.argv[4]

# Function to convert timestamps to number of seconds
def timestamp(time, file, lineNo):
	if (":" in time and "." in time 
		and ":." not in time and ".:" not in time
		and time.count(".") == 1 and time.count(":") == 1):	# If formatted correctly, eg. 0:10.2790
		time = re.sub(r"[^\d.:]", "", time)
		timeUnits = time.split(":")
		minutes = float(timeUnits[0])
		seconds = float(timeUnits[1])
	else:						# If formatted incorrectly (corpus error), eg. 0.10.2790
		# Report the error
		with open("corpuserrors.txt", "a") as errorfile:
			error = file + " Line " + str(lineNo) + " The timestamp is formatted incorrectly. Timestamp: " + time + "\n"
			errorfile.write(error)

		# Fix it
		if re.search(r"[\D]", time):	# If contains something that is not a digit
			time = re.sub("\D", ".", time)
			timeUnits = time.split(".")
			minutes = float(timeUnits[0])
			if time[-3] == ".":
				lastTwo = time[-2:]
				time = time[:-3]
				time = time + lastTwo

			if len(timeUnits[1]) > 2: # Corpus error, eg. 2:441955
				seconds = float(timeUnits[1][:2] + "." + timeUnits[1][2:])
			else:
				seconds = float(timeUnits[1] + "." + timeUnits[2])
		else:	# eg. 411805032
			decimal = time[-4:]
			time = time[:-4]
			seconds = float(time[-2:] + "." + decimal)
			time = time[:-2]
			minutes = float(time)

	totalSeconds = float('%.4f'%(seconds + (60*minutes)))
	return totalSeconds

# Function to convert number of seconds into timestamps
def detimestamp(time):
	totalMinutes = float(time)/60
	totalSplit = str(totalMinutes).split(".")
	minutes = totalSplit[0]
	totalSplit[1] = float("." + totalSplit[1])
	seconds = str('%.4f'%((totalSplit[1]*60)))
	if len(seconds.split(".")[0]) == 1:
		seconds = "0" + seconds
	timestamp =  str(minutes) + ":" + str(seconds)
	return timestamp


# Function to strip tags from text appropriately
def cleanText(text):
	# Deal with accents (specifically in French names, but this could be augmented for use with another language's corpus)
	text = re.sub(r"&(a|A)circumflex;", u"â", text)
	text = re.sub(r"&(e|E)circumflex;", u"ê", text)
	text = re.sub(r"&(i|I)circumflex;", u"î", text)
	text = re.sub(r"&(o|O)circumflex;", u"ô", text)
	text = re.sub(r"&(u|U)circumflex;", u"û", text)

	text = re.sub(r"&(e|E)acute;", u"é", text)

	text = re.sub(r"&(a|A)grave;", u"à", text)
	text = re.sub(r"&(e|E)grave;", u"è", text)

	text = re.sub(r"&(i|I)uml;", u"ï", text)
	text = re.sub(r"&(e|E)uml;", u"ë", text)
	text = re.sub(r"&(o|O)uml;", u"ö", text)

	text = re.sub(r"&(c|C)cedille;", u"ç", text)

	# Strip tags
	text = re.sub(r"foreign>.*</foreign", "", text)	# Foreign words
	#text = re.sub(r"@>.*</@", "", text)				# Changed names
	text = re.sub(r"(?<=@>).*(?=</@)", "beep_sound", text)
	text = re.sub(r"indig>.*</indig", "", text)		# Indigenous words
	text = re.sub(r"unclear>.*</unclear", "", text)	# Unclear words
	text = re.sub(r"O>.*</O", "", text)				# Untranscribed text
	text = re.sub(r"X>.*</X", "", text)				# Extra-corpus text
	text = re.sub(r"&>.*</&", "", text)				# Editorial comment
	text = re.sub(r"mention>|</mention", "", text)	# Mention
	text = re.sub(r"quote>|</quote", "", text)			# Quote
	text = re.sub(r"<.{1,3}>", "", text)				# All others
	text = re.sub(r"(.{1,2}>)|(<.{1,2})|(</.{1,2})", "", text)
	text = re.sub(r"(?<![a-zA-Z])-(?![a-zA-Z])", "", text)	# Deletes -, except when surrounded by alphabet, eg. keeps "twenty-seventh"
	text = re.sub(r"(?<![a-zA-Z])'(?![a-zA-Z])", "", text)	# Deletes ', except when surrounded by alphabet
	text = re.sub(ur"[^a-zA-Z\s'_âêîôûéàèïëö-]", "", text)

	text = " ".join(text.split())
	return text

# Function to get length of a wav file
def getWavLength(wav, wavDir):
	sampFreq, snd = wavfile.read(os.path.join(wavDir, wav))
	bit = 0
	if snd.dtype == "int16":
		bit = 15
	elif snd.dtype == "int32":
		bit = 31
	snd = snd / float((2.**bit))
	duration = snd.shape[0] / float(sampFreq) # Returns in milliseconds
	return duration

# Function to get the speaker's name from the metadata (replacing A, B, C...)
def getSpeaker(file, letter, sheet):
	#print "file being passed: " + file
	r = 0
	textcode = sheet.col(0)	# File name col
	for rowNo, row in enumerate(textcode):
		#print "cell being checked: " + sheet.cell_value(rowNo, 0)
		if sheet.cell_value(rowNo, 0) == file:
			r = rowNo
			#print sheet.cell_value(rowNo, 0)
			break
	speakerID = sheet.col(4)	# Speaker letter col
	letter = re.sub(r"[^a-zA-Z]", "", letter)
	while sheet.cell_value(r, 4) != letter:
		r = r + 1
	# Get first name
	if sheet.cell_value(r, 11) != "":
		first = sheet.cell_value(r, 11)
	else:
		first = "Placeholder1"
	# Get last name
	if sheet.cell_value(r, 12) != "":
		last = sheet.cell_value(r, 12)
	else:
		last = "Placeholder2"
	name = first + " " + last
	return name


if __name__ == '__main__':
	try:	# Set up corpus error file
		os.remove("corpuserrors.txt")
	except OSError:
		pass

	excel = xlrd.open_workbook(metadata)	# Load in metadata
	sheet = excel.sheet_by_index(1)

    # Loops through files and turns them into audio+transcription paired textgrids
	for file in os.listdir(transcription_text_source):
		if file[-4:] == ".txt":
			file_name = file.split(".")
			corresponding_wav = file_name[0] + ".wav"

			print "Processing " + file + " and " + corresponding_wav + "..."

			# Get length of the wav file
			duration = getWavLength(corresponding_wav, transcription_wav_source)

			# Make a textgrid for the file
			tg = TextGrid(maxTime = duration)

			lastEnd = 0			# Pointer
			speakers = {}		# Contains speakers as keys and end of time last spoken as values
			intervalTiers = {}

			# Get list of lines from transcript
			with open(os.path.join(transcription_text_source, file)) as f:
				s = f.read().replace('\r\n', '\n').replace('\r', '\n')
    			lines = s.split('\n')
	
			# Make an interval for each line
			for line in lines:
				lineNo = lines.index(line)
				line = line.rstrip()
				lineSplit = re.split(r">\s*<", line)

				empty = False
				if line == "gg" or line == "<I>":
					continue
				if line == "ERROR - transcript missing":
					print "The transcript for this file is missing."
					with open("corpuserrors.txt", "a") as errorfile:
								error = file + " Line " + line + "\n"
								errorfile.write(error)
					empty = True
					break

				# An example line
				# <$A> <ICE-CAN S3A-002 #1:1:A> <start=0:00.0000 end=0:02.0262>  <#> There should be three minutes

				if line != "" and lineSplit[0][1] == '$' and lineSplit[0][2] != 'Z':	# Speaker Z = editorial commentary
					letter = lineSplit[0]
					speaker = getSpeaker(file_name[0], letter, sheet)
					if "Placeholder1" in speaker and "Placeholder2" in speaker:
						speaker = speaker + " " + letter + " " + file_name[0]
					if speaker not in speakers:
						speakers[speaker] = 0	# Placeholder value
						# Make a text tier for the new speaker
						speakerTier = IntervalTier(speaker, 0, duration)
						intervalTiers[speaker] = speakerTier

					# Prepare to mark a new interval in the speaker tier
					# No timestamp = editorial commentary; ignore this iteration
					timeTag = lineSplit[2].split(" ")
					if (re.search(r"\d", timeTag[0]) != None 
						and re.search(r"\d", timeTag[1]) != None):
						if "=" not in timeTag[0]:
							with open("corpuserrors.txt", "a") as errorfile:
								error = file + " Line " + str(lineNo) + " The time tag is formatted improperly: " + timeTag[0] + "\n"
								errorfile.write(error)
							startRaw = timeTag[0].strip("start")
						elif "=" not in timeTag[1]:
							with open("corpuserrors.txt", "a") as errorfile:
								error = file + " Line " + str(lineNo) + " The time tag is formatted improperly: " + timeTag[1] + "\n"
								errorfile.write(error)
							endRaw = timeTag[1].strip("end")
						else:		
							startRaw = timeTag[0].split("=")[1]
							endRaw = timeTag[1].split("=")[1]

						lastEnd_timestamp = detimestamp(lastEnd)
						startRaw = detimestamp(timestamp(startRaw, file, lineNo))

						# Simple corpus error check - given eg.
							# <start=5:32.6037 end=5:35.1838> followed immediately by
							# <start=5:53.1838 end=5:36.0438>
							# Just swap the two digits back that have been swapped
						if (lastEnd_timestamp.split(":")[1][0] == startRaw.split(":")[1][1] 
							and lastEnd_timestamp.split(":")[1][1] == startRaw.split(":")[1][0]
							and lastEnd_timestamp.split(":")[1][0] != lastEnd_timestamp.split(":")[1][1]):
							# Report the error
							with open("corpuserrors.txt", "a") as errorfile:
								error = file + " Line " + str(lineNo) + " The digits of the seconds seem to be accidentally swapped: " + lastEnd_timestamp + " is followed by " + startRaw + "\n"
								errorfile.write(error)

							# Fix it
							seconds = startRaw.split(":")[1].split(".")[1]
							startRaw = startRaw.split(":")[0] + ":" + lastEnd_timestamp.split(":")[1][0] + lastEnd_timestamp.split(":")[1][1] + "." + seconds

						# Another simple check - given eg.
							# <start=2:39.6100 end=2:43.4285> followed immediately by
							# <start=3:43.4314 end=2:44.3599>
							# Make the second's minute digit match the first; probably an accident
						if(((lastEnd_timestamp.split(":")[1].split(".")[0] == startRaw.split(":")[1].split(".")[0])
							or (int(lastEnd_timestamp.split(":")[1].split(".")[0])+1 == int(startRaw.split(":")[1].split(".")[0])))
							and lastEnd_timestamp.split(":")[0] != startRaw.split(":")[0]):
							# Report the error
							with open("corpuserrors.txt", "a") as errorfile:
								error = file + " Line " + str(lineNo) + " The minutes seem to be accidentally incorrect: " + lastEnd_timestamp + " is followed by " + startRaw + "\n"
								errorfile.write(error)

							# Fix it
							minutes = lastEnd_timestamp.split(":")[0]
							startRaw = minutes + ":" + " ".join(startRaw.split(":")[1:])

						start = timestamp(startRaw, file, lineNo)
						end = timestamp(endRaw, file, lineNo)

						# First 0-2 items are tags; remove these to access just the text
						lineSplit.pop(0)					
						lineSplit.pop(0)
						lineSplit.pop(0)
						text = " ".join(lineSplit)

						text = cleanText(text)	# Strip the extraneous tags


						# Now check for other corpus errors.
						switch = False
						if end < start: 	# Probably a simple mistake. Just swap start and end
							# Report the error
							with open("corpuserrors.txt", "a") as errorfile:
								error = file + " Line " + str(lineNo) + " The end time " + endRaw + " is less than the start time " + startRaw + "\n"
								errorfile.write(error)
							#print "@@@"
							temp = end
							end = start
							start = temp
							switch = True

						switch2 = False
						if start < speakers[speaker]:
							# If the start time for this speaker is less than the end time of
							# the last time this speaker spoke, move the start time to the old end time
							# Report the error if it's not a result of the previous if-block's change
							if switch == False:
								with open("corpuserrors.txt", "a") as errorfile:
									error = file + " Line " + str(lineNo) + " The start time for this speaker " + startRaw + " is less than the end time of when they last spoke " + detimestamp(speakers[speaker]) + "\n"
									errorfile.write(error)
							start = speakers[speaker]
							#print "fix! start: " + str(speakers[speaker]) + " end: " + str(end)
							switch2 = True

						switch3 = False
						if end < speakers[speaker]:
							# If the end time for this speaker is less than the end time of
							# the last time this speaker spoke, move the end time to the old end time
							# Report the error if it's not a result of the previous if-block's change
							if switch2 == False:
								with open("corpuserrors.txt", "a") as errorfile:
									error = file + " Line " + str(lineNo) + " The end time for this speaker " + endRaw + " is less than the end time of when they last spoke " + detimestamp(speakers[speaker]) + "\n"
									errorfile.write(error)
							end = speakers[speaker]
							#print "??? start: " + str(speakers[speaker]) + " end: " + str(end)
							switch3 = True

						if start == end:
							# If the start and end times for this speaker are the same,
							# presumably nothing has been said in this interval, so skip
							if switch3 == False:
								with open("corpuserrors.txt", "a") as errorfile:
									error = file + " Line " + str(lineNo) + " The start time for this speaker " + startRaw + " is the same as the end time " + endRaw + "\n"
									errorfile.write(error)
							#print "!!! start: " + str(speakers[speaker]) + " end: " + str(end)
							continue

						if start > duration or end > duration:
							# If either timestamp is greater than the duration of the whole file,
							# skip the interval unless it's the last; there's no good way to code around this it seems
							with open("corpuserrors.txt", "a") as errorfile:
								error = file + " Line " + str(lineNo) + " One of the timestamps exceeds the duration of the file. \n"
							#print "$$$ start: " + str(start) + " end: " + str(end) + " duration: " + str(duration)
							if line == lines[len(lines)-1] and end > duration:
								end = duration
							else:
								continue

						# Add the interval
						#print "Adding interval from speaker "+speaker+" from "+ str(start)+"("+detimestamp(start)+") to "+str(end)+"("+detimestamp(end)+"), \""+text[:50]+"..."
						intervalTiers[speaker].add(start, end, text)

						# Update pointers
						lastEnd = end
						speakers[speaker] = end

			with open("corpuserrors.txt", "a") as errorfile:
				errorfile.write("\n")

			if empty == False:
				# Add the speaker tiers, now populated with intervals, to the textgrid
				for key, value in intervalTiers.items():
					tg.append(value)

				# Write to a file
				exportName = file_name[0] + ".TextGrid"
				tg.write(os.path.join(transcription_output, exportName))
			#print "--------------------------------------------------------------------"

	print "Done."
	print ""
	print ""

				




				



