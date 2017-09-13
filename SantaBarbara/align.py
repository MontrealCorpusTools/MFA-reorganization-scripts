import sys
import shutil, os
import socket
import time
import logging
import platform
import csv
import statistics
from datetime import datetime

host = socket.gethostname()

class DummyArgs(object):
    def __init__(self):
        self.num_jobs = 12
        self.fast = False
        self.speaker_characters = 0
        self.verbose = False
        self.clean = True
        self.no_speaker_adaptation = True
        self.debug = False

args = DummyArgs()

if host == 'michael-laptop':
    MFA_REPO_PATH = r'D:\Dev\GitHub\Montreal-Forced-Aligner'
    args.corpus_directory = r'E:\Data\SB\mm_tg'
    args.dictionary_path = r'D:\Data\aligner_comp\dictionaries\dictionary_stressed.txt'
    args.output_directory = r'E:\Data\SB\aligned'
    args.temp_directory = r'E:\temp'
    args.acoustic_model_path = r'D:\Dev\GitHub\mfa-models\english.zip'
    args.num_jobs = 4
else:
    args.corpus_directory = '/media/share/corpora/SantaBarbara_for_MFA'
    args.dictionary_path = '/data/mmcauliffe/data/LibriSpeech/librispeech-lexicon.txt'
    args.output_directory = '/data/mmcauliffe/aligner-output/SantaBarbara'
    args.temp_directory = '/data/mmcauliffe/temp/MFA'
    args.acoustic_model_path = '/data/mmcauliffe/aligner-models/librispeech_models.zip'
    args.num_jobs = 6

sys.path.insert(0, MFA_REPO_PATH)


from aligner.command_line.align import align_corpus, fix_path, unfix_path


if __name__ == '__main__':
    fix_path()
    align_corpus(args)
    unfix_path()