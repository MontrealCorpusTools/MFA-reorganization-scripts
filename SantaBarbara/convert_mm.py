import os
import sys
import re
import wave
import subprocess
import socket
from textgrid.textgrid import Interval, IntervalTier, TextGrid

host = socket.gethostname()

if host == 'michael-laptop':
    data_dir = r'E:\Data\SB\SantaBarbara'
    output_dir = r'E:\Data\SB\mm_tg'
else:
    data_dir = r'/media/share/corpora/SantaBarbara'
    output_dir = r'/media/share/corpora/SantaBarbara_for_MFA'
os.makedirs(output_dir, exist_ok=True)


def clean_trans(trans):
    # Annotations inside ((X)) are comments, ignored
    if trans.startswith('(('):
        return [], False
    # Numbers and brackets align overlapping parts
    trans = re.sub(r'[0-9]', '', trans).replace('[', '').replace(']', '')

    # Punctuation is unnecessary, even when used to mark something linguistically (something pitch perception related)
    trans = re.sub(r'[.,!?]', '', trans)

    # Laughter length is marked by number of @'s, not necessary
    trans = re.sub(r'\s@+\s@+(\s@+\s)*', ' @ ', trans)

    trans = trans.split()
    new_trans = []
    if not trans:
        return [], False
    # (H) annotates breath (= is long)
    breath_start = trans[0] in ['(H)', '(H)=']
    for t in trans:
        skip = False
        # Punctuation that is used to mark continuations or small pauses in utterances, unnecessary

        for skip_mark in ['...', '--', '__', '(H)', '(H)=', '(Hx)', '..', 'XX', '(TSK)', '(SWALLOW)', '&', '+']:
            if t.startswith(skip_mark):
                skip = True

        # Bracketing is not useful for alignment, usually voice quality notes (laughter, etc)
        if t.endswith('>') or t.startswith('<') or t in ['-', 'X']:
            skip = True

        # % marks a break of some kind, not necessary for the aligner
        if '%' in t:
            skip = True
        if skip:
            continue

        # Words ending in a dash (or for some annotators an underscore) are cutoffs,
        # put them in [] for the aligner to mark as UNK

        # Tilde marks excised names, likewise better to specify as UNK

        if t.endswith('-') or t.endswith('_') or t.startswith('~'):
            t = '[' + t.replace('_', '-') + ']'
        t = re.sub(r'^_', '', t)

        # Words produced while laughing often have laugh markers at the beginning or end, not necessary for alignment
        if t.startswith('@'):
            m = re.search(r'\w', t)
            if m is None:
                t = '(LAUGH)' # Make laughter more similar to other non speech sounds
            else:
                t = re.sub(r'^@', '', t)
        if t.endswith('@'):
            t = re.sub(r'@$', '', t)

        # = is a length marker, wholly unnecessary
        t = t.replace('=', '')

        # some annotators use underscore instead of dash for compound words, standardizes them to dash
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
    # Extract only channel one (both channels have identical microphone source)
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
                if len(line) < 3:
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
                # There are many weird speaker notes for multiple talkers or environmental noise, not necessary to keep
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

                    # Start a new segment when the current annotation starts with a breath (small, reliable pause)
                    # Or when it's been longer than 200ms since the speaker's last annotation
                    if breath_start or t[0] - cur_interval.maxTime > 0.2:
                        begin, end = t[0], t[1]
                        if begin != end:
                            if breath_start:
                                # Adjust the boundaries to be inside of the breath
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
            if cur_interval.maxTime > duration:
                cur_interval.maxTime = duration
            intervals[s].addInterval(cur_interval)
        print(list(intervals.keys()))
        print([len(x) for x in intervals.values()])
        tg = TextGrid(maxTime=duration)
        for k, v in intervals.items():
            tg.append(v)
        tg.write(tg_path)

        copy_wav_path(wav_path, out_wav_path)
