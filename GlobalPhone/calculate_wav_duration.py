
import os
import shutil
import re
import sys
import soundfile

full_names = {
                'AR': 'Arabic',
                'BG': 'Bulgarian',
                'CH': 'Mandarin',
                'WU': 'Cantonese',
                'CR': 'Croatian',
                'CZ': 'Czech',
                'FR': 'French',
                'GE': 'German',
                'HA': 'Hausa',
                'JA': 'Japanese',
                'KO': 'Korean',
                'RU': 'Russian',
                'PO': 'Portuguese',
                'PL': 'Polish',
                'SP': 'Spanish',
                'SA': 'Swahili',
                'SW': 'Swedish',
                'TA': 'Tamil',
                'TH': 'Thai',
                'TU': 'Turkish',
                'VN': 'Vietnamese',
                'UA': 'Ukrainian'
                }

data_directory = r'/media/share/corpora/GP_for_MFA'


def get_wav_info(file_path):
    with soundfile.SoundFile(file_path, 'r') as inf:
        n_channels = inf.channels
        subtype = inf.subtype
        bit_depth = int(subtype.replace('PCM_', ''))
        frames = inf.frames
        sr = inf.samplerate
        duration = frames / sr
    return {'num_channels': n_channels, 'type': subtype, 'bit_depth': bit_depth,
            'sample_rate' : sr, 'duration': duration}


if __name__ == '__main__':
    for lang in full_names.keys():
        lang_dir = os.path.join(data_directory, lang)
        speaker_dirs = os.listdir(lang_dir)
        num_speakers = len(speaker_dirs)
        duration = 0
        for s in speaker_dirs:
            speak_dir = os.path.join(lang_dir, s)
            for f in os.listdir(speak_dir):
                if not f.endswith('.wav'):
                    continue
                wav_path = os.path.join(speak_dir, f)
                wav_info = get_wav_info(wav_path)
                duration += wav_info['duration']
        print(lang)
        print('Num speakers:', num_speakers)
        num_minutes = duration / 60
        num_hours = num_minutes / 60
        print('Duration:', num_hours)
