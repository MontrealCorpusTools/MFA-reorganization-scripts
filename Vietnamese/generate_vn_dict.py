import os
import re
from vPhon.vPhon import create_dictionary, save_dictionary
from textgrid import TextGrid

VN_dict_path = r'D:\Data\Vietnamese\lexicon_nosil.txt'
new_dict_path = r'D:\Data\Vietnamese\vn_dict_narrow.txt'
data_dir = r'D:\Data\Vietnamese\Brunelle_corpus'

glottal = False
cao = False
pham = False
dialect = 's'
tokenize = False
palatals = False


def get_words():
    words = set()
    with open(VN_dict_path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.split()
            words.add(line[0])
    return words


def get_corpus_words():
    files = os.listdir(data_dir)
    words = set()
    for f in files:
        if not f.endswith('.TextGrid'):
            continue
        print(f)
        tg = TextGrid()
        tg.read(os.path.join(data_dir, f))
        for t in tg:
            for i in t:
                sentence = i.mark.strip()
                if sentence == '':
                    continue
                sentence = sentence.split()
                for w in sentence:
                    w = re.sub(r'\W', '', w)
                    if not w:
                        continue
                    words.add(w.lower())
    return words


if __name__ == '__main__':
    words = get_corpus_words()
    text = [sorted(words)]
    dictionary = create_dictionary(text, glottal=glottal, cao=cao, pham=pham, dialect=dialect, tokenize=tokenize,
                                   palatals=palatals)
    save_dictionary(dictionary, new_dict_path)
