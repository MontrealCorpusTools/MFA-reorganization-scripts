
from vPhon.vPhon import create_dictionary,save_dictionary

VN_dict_path = r'D:\Vietnamese\lexicon_nosil.txt'
new_dict_path = r'D:\Vietnamese\vn_dict.txt'

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

if __name__ == '__main__':
    words = get_words()
    text = [sorted(words)]
    dictionary = create_dictionary(text,glottal=glottal, cao=cao, pham=pham,dialect=dialect, tokenize=tokenize,palatals=palatals)
    save_dictionary(dictionary, new_dict_path)