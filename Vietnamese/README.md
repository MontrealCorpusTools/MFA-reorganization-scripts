# Vietnamese alignment

Pronunciation dictionaries
==========================

There are two ways to generate a pronunciation dictionary for aligning Vietnamese.
The first is to use Michael McAuliffe's updated version of [vPhon](https://github.com/mmcauliffe/vPhon) (original author: Jamese Kirby).
This is a package that contains functions for transforming Vietnamese orthography into IPA.
To use it, you will have to write a script like the `generate_vn_dict.py` script in this directory.

The second way is to use MFA's G2P capabilities and a pre-trained model to generate a dictionary.
There is are two models.  The first is a pre-trained G2P model for transforming Vietnamese orthography to IPA following vPhon's rules.
This model was trained by extracting the list of words in the GlobalPhone dictionary, and then running
vPhon on each entry to generate a new pronunciation dictionary.  This model had an accuracy of 98.4% when validating on
10% of the dictionary and training on 90% of the dictionary (the actual models linked below use all of the dictionary as training).
This dictionary was then used to train the G2P model.
The second G2P model was trained on the original pronunciations that use GlobalPhone's phone set.  This model had an accuracy of 98.0%
when performing validation.

[IPA (vPhon Southern Vietnamese)](http://mlmlab.org/mfa/mfa-models/g2p/vietnamese_vphon_south_g2p.zip)
[GlobalPhone](http://mlmlab.org/mfa/mfa-models/g2p/vietnamese_g2p.zip)

Brunelle Corpus reorganization
==============================

The `reorganization.py` script transforms the original TextGrids of the corpus of Southern Vietnamese that Marc Brunelle
has into MFA format.  Some of the TextGrids have speaker turns encoded in a tier, rather than a function of tier name,
so this script regenerates TextGrids to have separate tiers for each speakers.  Prior to running this script, I also deleted
all tiers that were not relevant to alignment.

Aligning
========

Aligning a Vietnamese corpus is straightforward once the TextGrids are in the input format for MFA.  Following the MFA
documentation (http://montreal-forced-aligner.readthedocs.io/en/stable/aligning.html#align-using-only-the-data-set),
the corpus can be aligned by:

```
bin/mfa_train_and_align corpus_directory dictionary_path output_directory
```

Here we use train and align to generate acoustic models based on the data set (these models can be saved for future use with
the `-o /path/to/save/model.zip` flag).  There are acoustic models based on the GlobalPhone Vietnamese corpus available
[here](http://mlmlab.org/mfa/mfa-models/vietnamese.zip), but the speakers have a mix of dialects.