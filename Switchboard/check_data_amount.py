import xml.etree.ElementTree as ET
import textgrid as tg
import re
import sys
import os
from pathlib import Path
from collections import defaultdict
"""
check to see how much data would be lost if we ignored segments that cause problems
(very small percentage)
"""

class Word(object):
    """word object to keep track of words"""
    def __init__(self, start, end, label):
        super(Word, self).__init__()
        self.start = start
        self.end = end
        self.label = label

class Phone(object):
    """phone object to keep track of phones"""
    def __init__(self, start, end, label):
        super(Phone, self).__init__()
        self.start = start
        self.end = end
        self.label = label
        
def get_words_phones(word_phone_file, wordsp):
    """
    take a word or phone file, read the xml, parse it into ordered tuples of (start, end, label)

    Parameters
    ----------
    word_phone_file: str
        the filename of the xml file to read
    wordsp: bool
        True if file is a word file, false if a phones file

    Returns
    -------
    ordered_tups: list of tuples
        list of  (start, end, label) tuples for each word/phone
    """
    tree = ET.parse(word_phone_file)
    root = tree.getroot()
    j = 0
    ordered_tups = []
    for child in root:
        start = child.attrib['{http://nite.sourceforge.net/}start']
        end = child.attrib['{http://nite.sourceforge.net/}end']
        if not wordsp:
            label = child.text
        else:
            label = child.attrib['orth']
        j+=1
        ordered_tups.append( (start,end,label) )

    return (ordered_tups, j)

def get_lists(phone_file, word_file):
    """
    takes the names of a word file and phone file, gets the tuples
    turns each tuple into a word/phone object, adds silences

    Parameters
    ----------
    phone_file: str
        path to the .phones file
    word_file
        path to the .phonwords file

    Returns
    -------
    tuple
        (list of phones, list of words, end of the last phone, end of the last word, number of phones, number of words)
    """
    all_phones_a = get_words_phones(phone_file, False)
    final_phone_end = all_phones_a[0][-1][1]
    phone_length = all_phones_a[1]
    phone_list = []

    for phone_tup in all_phones_a[0]:
        phone_list.append(Phone(phone_tup[0], phone_tup[1], phone_tup[2]))

    all_words_a = get_words_phones(word_file,True)
    final_word_end = all_words_a[0][-1][1]    
    word_list = []

    for i,word_tup in enumerate(all_words_a[0]):
        word_end = word_tup[1]
        word_phones = []
        double = False
        try:
            if word_end != all_words_a[0][i+1][0]:
                difference = float(all_words_a[0][i+1][0]) - float(word_end)
                if difference < 0:
                    print("Error")
                w1 = Word(word_tup[0], word_end, word_tup[2])
                w2 = Word(word_tup[1], round(float(word_tup[1])+ difference, 6), "<SIL>")
                word_list.append(w1)
                word_list.append(w2)
                double = True
            else:
                w1 = Word(word_tup[0], word_end, word_tup[2])
                word_list.append(w1)

        except IndexError:
            pass
    return (phone_list, word_list, final_phone_end, final_word_end, phone_length, len(word_list))

def convert(word_file_a, phone_file_a,word_file_b, phone_file_b, textgrid_file):
    """
    given the word and phone files for speakers a and b, converts them into one textgrid file

    Parameters
    ----------
    word_file_a : str
        path to .A.phonwords file
    phone_file_a : str
        path to .A.phones file
    word_file_b : str
        path to B.phonwords file
    phone_file_b : str
        path to B.phones file
    textgrid_file :  str
        path to desired resulting textgrid

    """
    error_count =0

    tup_a = get_lists(phone_file_a, word_file_a)
    tup_b = get_lists(phone_file_b, word_file_b)

    phone_list_a, word_list_a, final_phone_end_a, final_word_end_a, phone_length_a, word_length_a = tup_a[0], tup_a[1], tup_a[2], tup_a[3], tup_a[4], tup_a[5]
    phone_list_b, word_list_b, final_phone_end_b, final_word_end_b, phone_length_b, word_length_b = tup_b[0], tup_b[1], tup_b[2], tup_b[3], tup_b[4], tup_b[5]

    phones_words = [phone_list_a, word_list_a, phone_list_b, word_list_b]

    all_tiers = []
    textgrid = tg.TextGrid()
    phone_tierA = tg.IntervalTier(name = "phones_A")
    word_tierA = tg.IntervalTier(name = "words_A")
    all_tiers.append(phone_tierA)
    all_tiers.append(word_tierA)

    phone_tierB = tg.IntervalTier(name = "phones_B")
    word_tierB = tg.IntervalTier(name = "words_B")
    all_tiers.append(phone_tierB)
    all_tiers.append(word_tierB)

    for i,tier in enumerate(all_tiers):
        for element in phones_words[i]:
            try:
                tier.add(float(element.start), float(element.end), element.label)
            except ValueError:
                error_count +=1 
        textgrid.append(tier)

    # textgrid.write(textgrid_file)

    return (error_count, int(phone_length_b) + int(phone_length_a))

# if you want to redo some conversions because of transcription errors in xml, add to list ones you 
# do not want to redo 
EXCLUDE = []


# list of failed conversions
not_converted = []

def convert_all(input_dir, output_dir):
    """
    convert a whole directory of xml files

    Parameters
    ----------
    input_dir : str
        path to the directory containing .phonwords files
    output_dir : str
        desired location of the output textgrids 
    """
    all_phones = []
    errors = defaultdict(int)
    succ = 0
    total = 0
    with open("not_converted.txt") as f1:
        to_conv = [x.split('\t')[0] for x in f1.readlines()]
    for root, dirs, files in os.walk(input_dir, topdown=True):

        for file in sorted(files):
                num_name = file.split(".")[0]
                # print(num_name)
                just_num = int(num_name[2:])
                if just_num in range(0,1):
                    continue
                # if just_num not in to_conv:
                #     continue
                phone_dir = os.path.join(str(Path(root).parent), 'phones')


                A_phone_name = os.path.join(phone_dir, num_name+".A.phones.xml")
                A_phonwords_name = os.path.join(root, num_name+".A.phonwords.xml")
                B_phone_name = os.path.join(phone_dir, num_name+".B.phones.xml")
                B_phonwords_name = os.path.join(root, num_name + ".B.phonwords.xml")
                textgrid_name = num_name[0:2]+"0"+num_name[2:]+ ".textgrid"
                tg_output = os.path.join(output_dir, textgrid_name)
                try:
                    c = convert(A_phonwords_name, A_phone_name, B_phonwords_name, B_phone_name, tg_output)
                    errors[num_name] = c[0]
                    all_phones.append(c[1])
                    succ +=1 
                except (ValueError, IndexError) as e:
                    not_converted.append((num_name,e))
                total +=1

    # print("percent converted: {}".format(succ/total))
    print("total errors: {}".format(sum(errors.values())))
    print("average errors per file {}".format(sum(errors.values())/len(errors.keys())))
    print("total number of phones: {}".format(sum(all_phones)))

if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    convert_all(input_dir, output_dir)
    print(len(not_converted))
    with open("not_converted.txt","a") as f1:
        for nc in not_converted:
            f1.write(nc[0] + "\t" + str(nc[1]) + "\n")

# convert("/Volumes/data/corpora/nxt_switchboard_ann/xml/phonwords/sw2005.A.phonwords.xml",
#     "/Volumes/data/corpora/nxt_switchboard_ann/xml/phones/sw2005.A.phones.xml", 
#     "/Volumes/data/corpora/nxt_switchboard_ann/xml/phonwords/sw2005.B.phonwords.xml",
#     "/Volumes/data/corpora/nxt_switchboard_ann/xml/phones/sw2005.B.phones.xml", 
#     "/Users/elias/SPADE/sw2005.textgrid")



# convert("/Volumes/data/corpora/nxt_switchboard_ann/xml/phonwords/sw2008.A.phonwords.xml",
#     "/Volumes/data/corpora/nxt_switchboard_ann/xml/phones/sw2008.A.phones.xml", 
#     "/Volumes/data/corpora/nxt_switchboard_ann/xml/phonwords/sw2008.B.phonwords.xml",
#     "/Volumes/data/corpora/nxt_switchboard_ann/xml/phones/sw2008.B.phones.xml", 
#     "/Users/elias/SPADE/sw2008.textgrid")