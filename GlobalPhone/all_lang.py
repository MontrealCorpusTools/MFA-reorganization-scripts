
import os
import shutil
import re
import sys

from gp_utils import lang_encodings, globalphone_prep, globalphone_dict_prep

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

globalphone_dir = r'/media/share/corpora/GlobalPhone'

base_dirs = {k: os.path.join(globalphone_dir, v) for k,v in full_names.items()}

source_dirs = {k: os.path.join(base_dirs[k], v) for k,v in full_names.items()}

data_directory = r'/media/share/corpora/GP_for_MFA'

data_dirs = {k: os.path.join(data_directory, k) for k,v in source_dirs.items()}

dict_paths = {k: os.path.join(base_dirs[k],
                            '{}_Dict'.format(v),
                            '{}-GPDict.txt'.format(v))
                    for k,v in full_names.items()}

if __name__ == '__main__':
    for k in sorted(full_names.keys()):
        if not os.path.exists(source_dirs[k]):
            print(source_dirs[k],"not found")
            continue
        print(k)

        globalphone_dict_prep(source_dirs[k],dict_paths[k], data_dirs[k], k)

        globalphone_prep(source_dirs[k], data_dirs[k], k)

