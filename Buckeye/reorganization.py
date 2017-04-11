import sys
sys.path.insert(0, r'D:\Dev\GitHub\PolyglotDB')
import os
import re
import time
import wave
from statistics import mean
from shutil import copyfile

from textgrid import TextGrid, IntervalTier

from polyglotdb import CorpusContext
import polyglotdb.io as pgio
from acousticsim.utils import extract_audio

path_to_buckeye = r'D:\Data\VIC\Speakers'
out_dir = r'D:\Data\VIC\TextGrids'
mfa_out_dir = r'D:\Data\VIC\MFA_TextGrids'
lab_out_dir = r'D:\Data\VIC\prosodylab_format'

dictionary_path = r'D:\Dev\GitHub\aligner-comparison\aligning\librispeech_models\dictionary'

words = set()

with open(dictionary_path, 'r', encoding='utf8') as f:
    for line in f:
        words.add(line.split()[0].lower())

print(len(words))

connection_kwargs = {'graph_host':'localhost', 'graph_port': 7474,
            'graph_user': 'neo4j', 'graph_password': 'test'}

def call_back(*args):
    args = [x for x in args if isinstance(x, str)]
    if args:
        print(' '.join(args))

reset = False



with CorpusContext('buckeye', **connection_kwargs) as c:
    if reset:
        c.reset()
        beg = time.time()
        parser = pgio.inspect_buckeye(path_to_buckeye)
        parser.call_back = call_back
        c.load(parser, path_to_buckeye)
        end = time.time()
        print('Time taken: {}'.format(end - beg))
        if not 'utterance' in c.annotation_types:
            c.encode_pauses(r'^(<SIL>|<IVER.*|\{B_TRANS\}|\{E_TRANS\}|<VOCNOISE>)$', call_back = call_back)

            c.encode_utterances(min_pause_length = 0.15, call_back = call_back)

    if False:
        c.reset_utterances()
        c.reset_pauses()
        c.encode_pauses(r'^(<SIL>|<IVER.*|\{B_TRANS\}|\{E_TRANS\}|<VOCNOISE>)$', call_back = call_back)

        c.encode_utterances(min_pause_length = 0.15, call_back = call_back)

    durations = []
    unk_pattern = re.compile(r'^[<{]')
    ignored = 0
    not_ignored = 0
    for d in c.discourses:
        print(d)
        speaker = d[:3]
        tg_dir = os.path.join(mfa_out_dir, speaker)
        lab_dir = os.path.join(lab_out_dir, speaker)
        os.makedirs(tg_dir, exist_ok = True)
        os.makedirs(lab_dir, exist_ok = True)
        full_tg_dir = os.path.join(out_dir, speaker)
        os.makedirs(full_tg_dir, exist_ok = True)
        tg_path = os.path.join(tg_dir, d + '.TextGrid')
        full_tg_path = os.path.join(full_tg_dir, d+ '.TextGrid')
        wav_path = os.path.join(path_to_buckeye, speaker, d + '.wav')
        new_wav_path = os.path.join(tg_dir, d + '.wav')
        with wave.open(wav_path, 'rb') as wf:
            duration = wf.getnframes() / wf.getframerate()
        if not os.path.exists(new_wav_path):
            copyfile(wav_path, new_wav_path)
        tg = TextGrid(maxTime = duration)
        q = c.query_graph(c.utterance).filter(c.utterance.discourse.name == d).order_by(c.utterance.begin)
        q = q.preload(c.utterance.word, c.utterance.phone)
        utterance_tier = IntervalTier(name = speaker, maxTime = duration)
        word_tier = IntervalTier(name = 'words', maxTime = duration)
        phone_tier = IntervalTier(name = 'phones', maxTime = duration)
        for u in q.all():
            transcription = [(x._type_node['label'], x.begin) for x in u.word if x._type_node['label'] not in ['<NOISE>', '<VOCNOISE>']]
            if not transcription:
                continue
            if any(unk_pattern.match(x[0]) is not None for x in transcription) or any(x[0] not in words for x in transcription):
                ignored += 1
                continue
            not_ignored += 1
            #transcription = [x.label for x in sorted(u.word, key = lambda x: x.begin)]
            #print(transcription)
            if len(transcription) < 3 and u.duration > 25:
                continue
            if u.duration > 25:
                print(d, u.duration)
                print([(x._type_node['label'], x.begin, x.duration) for x in u.word])
                error
            transcription = ' '.join(x[0] for x in transcription)
            begin = u.begin - 0.075
            if begin < 0:
                begin = 0
            end = u.end + 0.075
            if end > duration:
                end = duration
            utterance_tier.add(begin, end, transcription)
            utt_duration = end - begin
            utt_name = '{}_{}_{}'.format(d, begin, end)
            utt_wav_path = os.path.join(lab_dir, utt_name + '.wav')
            if not os.path.exists(utt_wav_path):
                extract_audio(wav_path, utt_wav_path, begin, end, padding = 0)
            lab_path = os.path.join(lab_dir, utt_name + '.lab')
            with open(lab_path, 'w') as f:
                f.write(transcription)
            trans_path = os.path.join(lab_dir, utt_name + '.txt')
            with open(trans_path, 'w') as f:
                f.write('{}\t{}\t0\t{}\t{}'.format(speaker, speaker, utt_duration, transcription))
            utt_tg_path = os.path.join(lab_dir, utt_name + '.TextGrid')
            utt_tg = TextGrid(maxTime = utt_duration)
            utt_word_tier = IntervalTier(name = 'words', maxTime=utt_duration)
            utt_phone_tier = IntervalTier(name = 'phones', maxTime=utt_duration)
            for w in u.word:
                label = w._type_node['label']
                if label in ['<NOISE>', '<VOCNOISE>']:
                    continue
                end = w.end
                if end > duration:
                    end = duration
                word_tier.add(w.begin, end, label)
                utt_word_tier.add(w.begin - begin, end - begin, label)
            for p in u.phone:
                label = p._type_node['label']
                end = p.end
                if end > duration:
                    end = duration
                try:
                    phone_tier.add(p.begin, end, label)
                    utt_phone_tier.add(p.begin - begin, end - begin, label)
                except ValueError:
                    print(label, p.begin, p.end, duration)
                    raise
            durations.append(u.duration)
            utt_tg.append(utt_word_tier)
            utt_tg.append(utt_phone_tier)
            utt_tg.write(utt_tg_path)
        tg.append(utterance_tier)
        tg.write(tg_path)
        tg.append(word_tier)
        tg.append(phone_tier)
        tg.write(full_tg_path)

print(ignored, not_ignored)