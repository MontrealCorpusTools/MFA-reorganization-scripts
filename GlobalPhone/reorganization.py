import os
import shutil

base_dir = '/data/mmcauliffe/aligner-output/CR'

output_dir = '/media/share/corpora/GP_aligned/CR'

for f in os.listdir(base_dir):
    in_path = os.path.join(base_dir, f)
    speaker = f.split('_')[0]
    out_path = os.path.join(output_dir, speaker, f)
    os.remove(out_path)
    shutil.copyfile(in_path, out_path)