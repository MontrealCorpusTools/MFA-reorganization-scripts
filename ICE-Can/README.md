# ICE-Canada Corpus

This folder contains 3 files for treating transcripts and audio files of the [ICE-Canada](https://dataverse.library.ualberta.ca/dvn/dv/VOICE) corpus before they can be aligned with the [Montreal Forced Aligner](http://montreal-forced-aligner.readthedocs.io/en/latest/index.html): ```mp3ToWav.py```, ```resample.praat```, and ```transcript_translate.py```. They should be run in this order.

## mp3ToWav.py

The ICE-Canada corpus contains some files in .mp3 that must first be converted into .wav format, which this script accomplishes.

### Prerequisites
* [PyDub](https://github.com/jiaaro/pydub), installed through ```pip install pydub```
* [ffmpeg](https://ffmpeg.org), see PyDub documentation for installation details

### Running
Place this script in a directory containing all the .wav files, and create a subdirectory and move all of the .mp3 files there. Then, run:

```python mp3ToWav.py mp3_dir```

This will place the newly converted .wav files into the directory with all the other .wav files.

## resample.praat

Some of the ICE-Canada corpus .wav files have an extremely high sampling rate that will not work with the aligner. This script downsamples the files to 44.1 kHz.

### Prerequisites
* [Praat](http://www.fon.hum.uva.nl/praat/)

### Running
Make sure there is a directory containing all the .wav files. Choose a separate directory where the downsampled files will be output. Then, in Praat, go to ```Praat > Open Praat Script``` and run the script with the desired parameters. (This may take a while.)

## translate_transcript.py
This script cleans the transcripts of the ICE-Canada corpus recordings, tags them by speaker as given by the corpus metadata, and converts them into a [TextGrid](http://www.fon.hum.uva.nl/praat/manual/TextGrid.html) format.

### Prerequisites
* [SciPy](https://github.com/scipy/scipy#installation), see documentation for installation details
* [textgrid](https://github.com/kylebgorman/textgrid), installed through ```pip install git+http://github.com/kylebgorman/textgrid.git```
* [xlrd](https://github.com/python-excel/xlrd), installed through ```pip install xlrd```

### Running

Make sure that there is a directory containing all the .wav files, a directory containing all the .txt transcript files, a desired output directory, and the metadata file (as downloadable with the rest of the corpus). Then, run:

```python translate_transcript.py txt_dir wav_dir output_dir metadata```