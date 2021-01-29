import os
from collections import defaultdict

full_names = {
                'AR': 'Arabic',
                'BG': 'Bulgarian',
                'CH': 'Mandarin',
                'CH_char': 'Mandarin',
                'EN': 'English',
                'WU': 'Cantonese',
                'CR': 'Croatian',
                'CZ': 'Czech',
                'FR': 'French',
                'FR_lexique': 'French',
                'FR_prosodylab': 'French',
                'GE': 'German',
                'GE_prosodylab': 'German',
                'HA': 'Hausa',
                'JA': 'Japanese',
                'KO': 'Korean',
                'KO_jamo': 'Korean',
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
                'UA': 'Ukrainian',
                }

root_dir = r'E:\Data\dictionaries\raw'

output_dir = r'E:\Data\dictionaries\cleaned'

os.makedirs(output_dir, exist_ok=True)


def load_file(path):
    grapheme_set = set()
    phone_set = set()
    regular = defaultdict(set)
    weird = defaultdict(set)
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if '\t' in line:
                word, pron = line.split('\t')
            else:
                word, pron = line.split(' ', maxsplit=1)
            word = word.lower()
            pron = tuple(x for x in pron.split(' ') if x)
            skip = False
            for p in weird_phone_set:
                if p in pron:
                    skip = True
            if skip:
                continue
            is_weird = False
            for c in weird_char_set:
                if c in word:
                    is_weird = True
            if word.endswith('-'):
                is_weird = True
            if is_weird:
                weird[word].add(pron)
            else:
                print(word, pron)
                regular[word].add(pron)
                grapheme_set.update(word)
                phone_set.update(pron)
    #print(weird)
    print(len(weird))

    print(len(regular))
    print(regular['zwei'])
    print('GRAPH', sorted(grapheme_set))
    print('PHONE', phone_set)
    return regular


def save_dictionary(word_dict, path):
    with open(path, 'w', encoding='utf8') as f:
        for word, v in word_dict.items():
            for pron in v:
                f.write('{}\t{}\n'.format(word, ' '.join(pron)))


for code, land in full_names.items():
    if code == 'AR':
        weird_char_set = ['<', '>', '.', '1', '2', '4', '5', '6', '8', '9', '0']
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'BG':
        continue
        weird_char_set = ['a', 'b', 'd', 'e', 'g', 'h', 'i', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'CH':
        continue
        weird_char_set = []
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'CH_char':
        continue
        weird_char_set = []
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'CR':
        continue
        weird_char_set = ["'"] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'CZ':
        continue
        weird_char_set = [')', '_', '2']
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'EN':
        continue
        weird_char_set = []
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'GE':
        continue
        weird_char_set = ['=', '%', '*', '<', ':', '$', '_', '!', '.', '~'] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'GE_prosodylab':
        continue
        weird_char_set = ['#']
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'FR':
        continue
        weird_char_set = []
        weird_phone_set = []
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'FR_lexique':
        continue
        weird_char_set = ['.']
        weird_phone_set = []
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'FR_prosodylab':
        continue
        weird_char_set = ['.']
        weird_phone_set = []
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'CR':
        continue
        weird_char_set = ['#']+ [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'HA':
        continue
        weird_char_set = []
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'JA':
        continue
        weird_char_set = ['９', '〇', '×', 'A', 'F', 'N', 'T', '・', '％', '＆', '（', '＋', '０', '１', '２', '３', '４', '５',
                          '７', '８', 'Ａ', 'Ｂ', 'Ｃ', 'Ｄ', 'Ｅ', 'Ｆ', 'Ｇ', 'Ｈ', 'Ｉ', 'Ｊ', 'Ｋ', 'Ｌ', 'Ｍ', 'Ｎ', 'Ｏ',
                          'Ｐ', 'Ｑ', 'Ｒ', 'Ｓ', 'Ｔ', 'Ｕ', 'Ｖ', 'Ｗ', 'Ｘ', 'Ｙ']
        weird_phone_set = []
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'KO':
        continue
        weird_char_set = ['e', 'i', 'n', 'o', 's'] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'KO_jamo':
        continue
        weird_char_set = ['e', 'i', 'n', 'o', 's'] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'PL':
        continue
        weird_char_set = [] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'PO':
        continue
        weird_char_set = ['�', '$', '&', '+', '.', '/', ':', '<', '>', '_', '`', '}'] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'RU':
        continue
        weird_char_set = ['c', 'v'] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'SA':
        continue
        weird_char_set = [] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'SP':
        continue
        weird_char_set = ['<', '>', '^'] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'SW':
        continue
        weird_char_set = ['&', '>'] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'TH':
        continue
        weird_char_set = [',', '.', '<', '>', '"', '-'] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'TU':
        continue
        weird_char_set = ['%', '&', '+', '.', ';', '=', '̇'] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'UA':
        continue
        weird_char_set = ['a', 'b', 'e', 'f', 'g', 'i', 'k', 'l', 'n', 'o', 'p', 'r', 's', 'u', 'w', '–'] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'VN':
        continue
        weird_char_set = ['.'] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)
    elif code == 'WU':
        continue
        weird_char_set = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'a', 'c', 'd', 'e', 'i', 'k', 'n', 'p', 'r', 's', 't', 'w', 'x'] + [str(x) for x in range(10)]
        weird_phone_set = ['+hGH']
        dict_path = os.path.join(root_dir, '{}_dictionary.txt'.format(code))
        new = load_file(dict_path)
        new_path = os.path.join(output_dir, '{}_cleaned.txt'.format(code))
        save_dictionary(new, new_path)