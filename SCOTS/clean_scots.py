#!/usr/bin/env python


# Cleans up SCOTS textgrids to be used with the MFA

# [CENSORED: forename]
# <vocallex desc=""eh"" />
# <gap reason=""inaudible"" />
# <unclear></unclear>
# <falsestart>wor-</falsestart>
# <trunc>wor-</trunc>
# [non lexical items, non linguistic events]

import os
import sys
import re
import subprocess
from textgrid import TextGrid, IntervalTier

input_dir = sys.argv[1]
output_dir = sys.argv[2]

os.makedirs(output_dir, exist_ok=True)


def cleanText(text):
    text = re.sub(r"<vocallex desc=\"\"", "", text)
    text = re.sub(r"\"\"\s/>", "", text)
    text = re.sub(r"(<unclear>|</unclear>)", "", text)
    text = re.sub(r"(<falsestart>|-<falsestart>)", "", text)
    text = re.sub(r"(<trunc>|-</trunc>)", "", text)
    text = re.sub(r"<note>.*</note>", "", text)

    text = re.sub(r"<vocal desc=\"\".*/>", "", text)
    text = re.sub(r"<censored type=\"\".*\"\" >.*</censored>", "beep_sound", text)
    text = re.sub(r"censored type.*censored", "beep_sound", text)
    text = re.sub(r"<gap reason=\"\".*\"\" \s/>", "", text)
    text = re.sub(r"vocallex desc", "", text)
    text = re.sub(r"(vocal desc.*\s|vocal desc.*\n|vocal desc.*\")", " ", text)
    text = re.sub(r"<vocal desc=\"\".*/>", "", text)
    text = re.sub(r"event desc.*\s", "", text)
    text = re.sub(r"(gap reason.*\s|gap reason.*\n|gap reason.*\")", " ", text)
    text = re.sub(r"falsestart", "", text)
    text = re.sub(r"<br />", "", text)

    text = re.sub(r"(?<![a-zA-Z])'(?![a-zA-Z])", "", text)  # Deletes ', except when surrounded by alphabet
    text = re.sub(r"(?<![a-zA-Z])-(?![a-zA-Z])", "",
                  text)  # Deletes -, except when surrounded by alphabet, eg. keeps "twenty-seventh"
    text = re.sub(r"[^a-zA-Z\s'_-]", "", text)
    text = re.sub(r"(^\'[a-zA-Z]|\s\'[a-zA-Z]|[a-zA-Z]\'\s|[a-zA-Z]\'\n|[a-zA-Z]\'$)", "", text)

    text = text.split()
    #for item in text:
    #    if len(item) == 1 and item in "bcdefghijklmnpqrstuvwxyz":
    #        item = ""
    text = " ".join(text)
    return text




if __name__ == '__main__':
    # Loop through all textgrids
    for file in os.listdir(input_dir):
        filePath = os.path.join(input_dir, file)
        outputPath = os.path.join(output_dir, file)
        if file.endswith(".TextGrid"):
            print("Processing " + file + "...")
            filePath = os.path.join(input_dir, file)
            tg = TextGrid()
            tg.read(filePath)  # Read into a textgrid

            # Clean the text
            for tier in tg.tiers:
                for interval in tier:
                    # print repr(interval.mark)
                    interval.mark = cleanText(interval.mark)
                    if interval.mark != "":
                        print(interval.mark)

            # Write to file
            tg.write(outputPath)
        elif file.endswith('.wav') and not os.path.exists(outputPath):

            subprocess.call(['sox', filePath, outputPath, 'rate', '16000'])
