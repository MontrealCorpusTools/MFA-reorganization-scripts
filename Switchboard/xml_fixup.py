import subprocess
import os


"""
interactive helper to open the broken xml files in Sublime Text and tell you which timepoint to fix
"""
phone_path ="/Volumes/data/corpora/nxt_switchboard_ann/xml/phones/"
words_path = "/Volumes/data/corpora/nxt_switchboard_ann/xml/phonwords"


with open("not_converted.txt") as f1:
    lines = f1.readlines()

for line in lines:
    splitline = line.split("\t")
    cont = input("file: {}, error: {}".format(splitline[0], splitline[1]))
    subprocess.call(['open','-a', '/Applications/Sublime Text.app/', os.path.join(phone_path, splitline[0] + ".A.phones.xml")])
    subprocess.call(['open', '-a', '/Applications/Sublime Text.app/', os.path.join(phone_path, splitline[0] + ".B.phones.xml")])
    cont = input("next: ")