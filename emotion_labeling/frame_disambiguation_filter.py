from nltk.corpus import framenet as fn
import pandas as pd
import numpy as np
import operator
from random import shuffle
import os
import json

SQS_df = pd.read_csv('emotion_labeling/static/frame_disambiguation/aggregated_SQS.csv')


def pick_and_get_frame_disambiguation_material(index, all_frames = False):
    row = SQS_df.loc[int(index)]
    if !all_frames:
        uas = row['unit_annotation_score']
        uas = uas[8:len(uas)-1]
        uas = json.loads(uas.replace("'", '"'))
        uas = sorted(uas.items(), key=operator.itemgetter(1), reverse = True)
        frame_list = []
        idx = 0
        while len(frame_list) <7:
            if uas[idx][0] != 'none':
                frame_list.append(uas[idx][0])
            idx = idx + 1
        shuffle(frame_list)
    else:
        uas = row['input.frames'].split(',')
        frame_list = [ua[2:] for ua in uas]


    frame_definitions = {}
    for frame in frame_list:
        fs = fn.frames('(?i)'+frame)
        for f in fs:
            if frame == f.name.lower():
                frame_definitions[frame] = f.definition
    frame = {
        'target_sentence' : row['input.sentence'],
        'target_word' : row['input.word_phrase'],
        'frame_definitions' : frame_definitions,
    }
    return frame
