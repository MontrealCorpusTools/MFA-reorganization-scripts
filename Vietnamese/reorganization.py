import os
import re
import sys
from textgrid import TextGrid, IntervalTier

sub_pattern = re.compile(r'\W+')

data_dir = r'D:\Data\Vietnamese\Brunelle_corpus'
noncollapsed_dir = r'D:\Data\Vietnamese\Brunelle_corpus\noncollapsed'

def reorg_original(f):
    print(f)
    tg_path = os.path.join(noncollapsed_dir, f)
    tg = TextGrid()
    tg.read(tg_path)
    new_tg = TextGrid(maxTime=tg.maxTime)
    new_tg_path = tg_path.replace('_original.TextGrid', '.TextGrid')
    sentence_tier = tg.getFirst('Sentences')
    speaker_tier = tg.getFirst('Speakers')
    speaker_tiers = {}
    for i in speaker_tier:
        if i.mark == '':
            continue
        if ',' in i.mark:
            continue
        if i.mark == 'Tân.':
            continue
        speaker_tiers[i.mark] = IntervalTier(i.mark, maxTime=tg.maxTime)
    for i in sentence_tier:
        if not i.mark.strip():
            continue
        duration = i.maxTime - i.minTime
        mid_point = i.minTime + duration / 2
        speaker_int = speaker_tier.intervalContaining(mid_point)
        speaker = speaker_int.mark
        if speaker == 'Tân.':
            speaker = 'Tan'
        if speaker == '':
            continue
        if len(speaker_tiers[speaker]) > 0 and speaker_tiers[speaker][-1].maxTime == i.minTime:
            speaker_tiers[speaker][-1].maxTime = i.maxTime
            speaker_tiers[speaker][-1].mark = speaker_tiers[speaker][-1].mark + ' ' + i.mark
        else:
            speaker_tiers[speaker].addInterval(i)
    for k, v in sorted(speaker_tiers.items()):
        new_tg.append(v)
    print(speaker_tiers.keys())
    new_tg.write(new_tg_path)

def reorg_noncollapsed(f):
    padding = 0.1
    print(f)
    tg_path = os.path.join(noncollapsed_dir, f)
    tg = TextGrid()
    tg.read(tg_path)
    new_tg = TextGrid(maxTime=tg.maxTime)
    new_tg_path = tg_path.replace(noncollapsed_dir, data_dir)
    for tier in tg.tiers:
        new_tier = IntervalTier(name=tier.name, maxTime=tg.maxTime)
        for i in tier:
            new_mark = sub_pattern.sub(' ', i.mark).strip()
            if not new_mark:
                continue
            new_begin = i.minTime - padding
            if new_begin < 0:
                new_begin = 0
            new_end = i.maxTime + padding
            if new_end > tg.maxTime:
                new_end = tg.maxTime
            try:
                new_tier.add(new_begin, new_end, new_mark)
            except ValueError:
                new_tier[-1].maxTime = new_end
                new_tier[-1].mark += ' ' + new_mark
        print(len(new_tier))
        new_tg.append(new_tier)
    new_tg.write(new_tg_path)

files = os.listdir(noncollapsed_dir)

for f in files:
    if not f.endswith('original.TextGrid'):
        continue
    reorg_original(f)

files = os.listdir(noncollapsed_dir)

for f in files:
    if f.endswith('original.TextGrid'):
        continue
    reorg_noncollapsed(f)

