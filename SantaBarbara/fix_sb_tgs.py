import re
import os

"""
fix SB textgrids to be in proper format for FAVE parser
"""

for root,dirs,files in os.walk("/Volumes/data/corpora/SantaBarbara_aligned"):
    for file in files:
        if file.endswith("TextGrid"):
            path = os.path.join(root,file)
            with open(path, 'r') as f1:
                file_content = f1.read()
            with open(path, "w") as f2:
                file_content = re.sub("- words", "- word", file_content)
                file_content = re.sub(">env","env", file_content)
                file_content = re.sub(">mac", "mac", file_content)
                file_content = re.sub("- phones", "- phone", file_content)

                f2.write(file_content)

