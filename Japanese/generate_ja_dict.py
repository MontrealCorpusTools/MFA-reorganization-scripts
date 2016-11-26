import os
import re
import sys
import romkan

phone_cleanup_pattern = re.compile(r'(UA_|SWA_|M_|\{| WB\}|\})')

def cleanup_transcription(phone_sequence):
    phone_sequence = phone_cleanup_pattern.sub('', phone_sequence).strip()
    return phone_sequence

def parse_dictionary_file(path):
    nonsil = set()

    word_cleanup_pattern = re.compile(r'\(\d+\)')
    line_break_pattern = re.compile(r'\}\s+')
    word_pattern = re.compile(r'^{([^{}]+)\s+')
    dictionary = {}
    word_characters = set()
    with open(path, 'r', encoding = 'utf8') as f:
        try:
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                try:
                    word, phones = line_break_pattern.split(line, maxsplit=1)
                except ValueError:
                    raise(Exception('There was a problem with the line \'{}\'.'.format(line)))
                if 'SIL' in phones or '+QK' in phones:
                    continue
                word = word[1:].strip()
                if '{' in word:
                    word = word_pattern.match(line)
                    word = word.groups()[0]
                    phones = word_pattern.sub('',line)
                word = word_cleanup_pattern.sub('', word)
                word = word.strip()
                #word = word.lower()
                word_characters.update(word)
                phones = cleanup_transcription(phones)
                matches = phones.split()
                if len(matches) == 2 and matches[0] == matches[1]:
                    matches = matches[:1]
                nonsil.update(matches)
                if word not in dictionary:
                    dictionary[word] = []
                dictionary[word].append(matches)
        except UnicodeDecodeError:
            s = f.readline()
            print(repr(s))
            print(f.readline())
            raise(Exception)
    return dictionary, nonsil, word_characters

def generate_japanese_dictionary(source_dir, dictionary):
    split_re = re.compile(r'[]、 ]+')
    cleanup_re = re.compile(r'[]{}]')
    kanasplit_re = re.compile(r'\[+')
    nnize_re = re.compile(r'n(?=[pbtdkgrwsczj]|$)')
    trl_dir = os.path.join(source_dir, 'trl')
    adc_dir = os.path.join(source_dir, 'adc')
    not_found = {}
    ignore = set(['nokoribuN', 'tamawatte', 'fuyukai'])
    endings = ['na', 'datta']
    new_dictionary = {}
    graphemes = set([])
    for filename in sorted(os.listdir(trl_dir)):
        print(filename)
        with open(os.path.join(trl_dir, filename), 'r', encoding = 'eucjp') as f:
            for line in f:
                if line.startswith(';'):
                    continue
                words = split_re.split(line)
                for w in words:
                    w = w.strip()
                    if not w:
                        continue
                    if w in ['。','、','}']:
                        continue
                    if w.startswith('＜'):
                        continue
                    kanji = None
                    kana = None
                    if '[' in w:
                        print(w)
                        w = cleanup_re.sub('',w)
                        kanji, kana = kanasplit_re.split(w)
                    else:
                        kana = w
                    #print(kanji,kana)
                    print(w)
                    print(kana)
                    romanji = romkan.to_roma(kana)
                    #print(romanji)
                    romanji = romanji.replace("n'", 'N')
                    romanji = nnize_re.sub(r'N', romanji)
                    try:
                        d = dictionary[romanji]
                        if kanji is not None:
                            new_dictionary[kanji] = d
                            graphemes.update(kanji)
                        new_dictionary[kana] = d
                        graphemes.update(kana)
                    except KeyError:
                        for e in endings:
                            if romanji.endswith(e):
                                to_lookup = romanji[:-len(e)]
                                try:
                                    print(dictionary[to_lookup] + dictionary[e])
                                except KeyError:
                                    if romanji not in not_found:
                                        not_found[romanji] = set()
                                    not_found[romanji].add(filename)
                                break
                        else:
                            if romanji not in not_found:
                                not_found[romanji] = set()
                            not_found[romanji].add(filename)
    return new_dictionary, graphemes, not_found

def save_dictionary(dictionary, path):
    with open(path, 'w', encoding = 'utf8') as f:
        for w, pronunciations in sorted(dictionary.items()):
            for p in pronunciations:
                outline = '{}\t{}\n'.format(w, ' '.join(p))
                f.write(outline)

def dict_prep():
    source_dir = r'D:\Data\GlobalPhone\Japanese\Japanese'
    path = r'D:\Data\GlobalPhone\Japanese\Japanese_Dict\Japanese-GPDict.txt'
    dict_dir =  r'D:\Data\GlobalPhone\output\JA\dict'

    dictionary, nonsil, word_characters = parse_dictionary_file(path)

    lexicon_path = os.path.join(dict_dir, 'original_dictionary.txt')
    save_dictionary(dictionary, lexicon_path)
    dictionary, word_characters, not_found = generate_japanese_dictionary(source_dir, dictionary)
    lexicon_path = os.path.join(dict_dir, 'new_dictionary.txt')
    save_dictionary(dictionary, lexicon_path)
    with open(os.path.join(dict_dir, 'not_found.txt'), 'w', encoding = 'utf8') as f:
        for w, files in sorted(not_found.items()):
            f.write('{}\t{}\n'.format(w, ', '.join(sorted(files))))


if __name__ == '__main__':
    dict_prep()