import os
import shutil

base_dir = '/data/mmcauliffe/aligner-output/CR'

output_dir = '/media/share/corpora/GP_aligned/CR'
main_dir = '/media/share/corpora/GP_for_MFA/CR/files'

for speaker in os.listdir(base_dir):
    s_dir = os.path.join(base_dir, speaker)
    for f in os.listdir(s_dir):
        in_path = os.path.join(base_dir, speaker, f)
        out_path = os.path.join(output_dir, speaker, f.replace('.TextGrid', '.wav'))
        if not os.path.exists(out_path):
            wav_path = out_path.replace(output_dir, main_dir)
            shutil.copyfile(wav_path, out_path)
        #if os.path.exists(out_path):
        #    os.remove(out_path)
        #shutil.copyfile(in_path, out_path)