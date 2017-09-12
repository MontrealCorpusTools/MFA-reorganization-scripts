# This Praat script will change the sample rate of all sound files in a given directory
# and save files with the new rate to another directory.
# Based on Mietta Lennes' script that does something similar, 
# https://github.com/FieldDB/Praat-Scripts/blob/master/change_sample_rate_of_sound_files.praat


form Change sample rate in sound files
   sentence Sound_file_extension .aif
   comment Directory path of input files:
   text input_directory  C:\tmp\
   comment Directory path of resampled files (old files will be overwritten!):
   text output_directory  C:\tmp\resampled\
   optionmenu Output_format: 1
   option AIFF
   option WAV
   positive New_sample_rate_(Hz) 22050
   positive Precision_(samples) 50
   comment (See the Praat manual for details on resampling.)
endform

strings = Create Strings as file list: "list", input_directory$ + "/*.wav"
numberOfFiles = Get number of strings
appendInfoLine: "Got number of strings"
for ifile to numberOfFiles
	selectObject: strings
	sound$ = Get string: ifile
	Read from file: input_directory$ + "/" + sound$
	objectname$ = selected$ ("Sound", 1)
	oldrate = Get sample rate
	if oldrate <> new_sample_rate
		printline Resampling 'input_directory$''sound$' to 'new_sample_rate' Hz...
		Resample... 'new_sample_rate' precision
	else
		printline Sample rate of 'input_directory$''sound$' is already 'new_sample_rate' Hz, copying this file...
	endif
	if output_format$ = "AIFF"
		Save as AIFF file: output_directory$ + "/" + objectname$ + ".aif"
	else
		Save as WAV file: output_directory$ + "/" + objectname$ + ".wav"
	endif
	Remove
	select Sound 'objectname$'
	Remove
endfor

select Strings list
Remove