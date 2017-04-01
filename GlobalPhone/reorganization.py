import os
import shutil

base_dir = '/data/mmcauliffe/aligner-output/CR'

output_dir = '/media/share/corpora/GP_aligned/CR'

for speaker in os.listdir(base_dir):
    s_dir = os.path.join(base_dir, speaker)
    for f in os.listdir(s_dir):
        in_path = os.path.join(base_dir, speaker, f)
        out_path = os.path.join(output_dir, speaker, f)
        if os.path.exists(out_path):
            os.remove(out_path)
        shutil.copyfile(in_path, out_path)