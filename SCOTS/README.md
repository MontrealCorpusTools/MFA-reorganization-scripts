# SCOTS Corpus

This folder contains files for treating transcripts and audio files of the [SCOTS](http://www.scottishcorpus.ac.uk) corpus before they can be aligned with the [Montreal Forced Aligner](http://montreal-forced-aligner.readthedocs.io/en/latest/index.html).

## clean_scots.py

The SCOTS transcripts are already in textgrid format, but they need some treatment before alignment, which this script accomplishes.

### Prerequisites
* [textgrid](https://github.com/kylebgorman/textgrid), installed through ```pip install git+http://github.com/kylebgorman/textgrid.git```

### Running
Place this script wherever you want, and ensure that all the textgrids are in their own directory and that there exists a desired output directory for the fixed transcripts. Then, run:

```python clean_scots.py textgrid_input_dir output_dir```

This will put all the fixed textgrid transcripts in their own directory.

