import os
import sys
import re
import wave
import subprocess
from textgrid.textgrid import Interval, IntervalTier, TextGrid

data_dir = r'/media/share/corpora/SantaBarbara'
output_dir = r'/media/share/corpora/SantaBarbara_for_MFA'
os.makedirs(output_dir, exist_ok=True)


def clean_trans(trans):
    if trans.startswith('(('):
        return [], False
    trans = re.sub(r'[0-9]', '', trans).replace('[', '').replace(']', '')
    trans = re.sub(r'[.,!?]', '', trans)
    trans = re.sub(r'\s@+\s@+(\s@+\s)*', ' @ ', trans)
    #trans = trans.replace('%', '')
    trans = trans.split()
    new_trans = []
    if not trans:
        return [], False
    breath_start = trans[0] in ['(H)', '(H)=']
    for t in trans:
        skip = False
        for skip_mark in ['...', '--', '__', '(H)', '(H)=', '(Hx)', '..', 'XX', '(TSK)', '(SWALLOW)', '&', '+']:
            if t.startswith(skip_mark):
                skip = True
        if t.endswith('>') or t.startswith('<') or t in ['-','X']:
            skip = True
        if '%' in t:
            skip = True
        if skip:
            continue
        if t.endswith('-') or t.endswith('_') or t.startswith('~'):
            t = '[' + t.replace('_', '-') + ']'
        t = re.sub(r'^_', '', t)
        if t.startswith('@'):
            m = re.search(r'\w', t)
            if m is None:
                t = '(LAUGH)'
            else:
                t = re.sub(r'^@', '', t)
        if t.endswith('@'):
            m = re.search(r'\w', t)
            if m is not None:
                t = re.sub(r'@$', '', t)
        #t = re.sub(r'\W+$', '', t)
        t = t.replace('=', '')
        t = t.replace('_', '-')
        if t:
            new_trans.append(t)
    return ' '.join(new_trans), breath_start

def get_duration(wav_path):
    with wave.open(wav_path, 'rb') as f:
        sr = f.getframerate()
        samp_count = f.getnframes()
        return samp_count / sr

def copy_wav_path(wav_path, out_path):
    if os.path.exists(out_path):
        return
    subprocess.call(['sox', wav_path, out_path, 'remix', '1'])


for root, directories, files in os.walk(data_dir):
    for trn in sorted(files):
        if not trn.endswith('.trn'):
            continue
        print(trn)
        tg_path = os.path.join(output_dir, trn.replace('.trn', '.TextGrid'))
        wav_path = os.path.join(root, trn.replace('.trn', '.wav'))
        if not os.path.exists(wav_path):
            continue
        out_wav_path = wav_path.replace(root, output_dir)
        duration = get_duration(wav_path)
        cur_speaker = None
        turns = []
        transcriptions = {}
        cur_turn = []
        speakers = set()
        with open(os.path.join(root, trn)) as f:
            for line in f:
                line = line.strip()
                line = line.split()
                begin, end = line[0], line[1]
                begin, end = float(begin), float(end)
                if begin == 0 and end == 0:
                    continue
                if ':' in line[2]:
                    speaker = line[2].strip().replace(':', '').upper()
                    ind = 3
                else:
                    speaker = ''
                    ind = 2
                if speaker:
                    if speaker != cur_speaker and cur_turn:
                        turns.append(cur_turn)
                        cur_turn = []
                    cur_speaker = speaker
                if cur_speaker in ['>ENV', 'MANY', 'X', 'KEN/KEV']:
                    continue
                speakers.add(cur_speaker)
                trans = ' '.join(line[ind:])
                cur_turn.append((begin, end, cur_speaker, trans))
                if cur_speaker not in transcriptions:
                    transcriptions[cur_speaker] = []
                transcriptions[cur_speaker].append((begin, end, trans))

        intervals = {x: IntervalTier(x, maxTime=duration) for x in speakers}
        for s, turns in transcriptions.items():
            cur_interval = None
            for t in turns:
                if cur_interval is None:
                    mark, breath_start = clean_trans(t[2])
                    if not mark:
                        continue
                    cur_interval = Interval(t[0], t[1], mark)
                else:
                    mark, breath_start = clean_trans(t[2])
                    if not mark:
                        continue
                    if t[0] < cur_interval.maxTime:
                        cur_interval.maxTime = t[0]
                    if breath_start or t[0] - cur_interval.maxTime > 0.2:
                        begin, end = t[0], t[1]
                        if begin != end:
                            if breath_start:
                                cur_interval.maxTime += 0.14
                                begin += 0.15
                            if begin > end:
                                end = begin + 0.001
                        intervals[s].addInterval(cur_interval)
                        cur_interval = Interval(begin, end, mark)
                    else:
                        cur_interval.mark += ' ' + mark
                        cur_interval.maxTime = t[1]
            if cur_interval is None:
                continue
            intervals[s].addInterval(cur_interval)
        print(intervals)
        print(list(intervals.keys()))
        print([len(x) for x in intervals.values()])
        tg = TextGrid(maxTime=duration)
        for k, v in intervals.items():
            tg.append(v)
        tg.write(tg_path)

        copy_wav_path(wav_path, out_wav_path)
