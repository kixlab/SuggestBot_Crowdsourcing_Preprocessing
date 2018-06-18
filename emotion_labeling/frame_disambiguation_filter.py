from nltk.corpus import framenet as fn
import pandas as pd
import numpy as np
import operator
from random import shuffle
import random
import os
import json
from urllib.request import urlopen
import urllib
import xmltodict
from .models import *
from django.db.models import Count, Min

INITIAL_TASK_SENTENCE = 2
TOTAL_SUB_TASK_NUM = 6
TARGET_TASK_NUM = 2
TASK_TIME_LIMIT = 1

SQS_df = pd.read_csv('emotion_labeling/static/frame_disambiguation/aggregated_SQS.csv')
exclude_list =[1, 4, 12, 14, 35, 38, 44, 47, 55, 80,
    100, 121, 126, 164, 211, 234, 239, 242, 244, 245, 270,
    293, 323, 341, 347, 361, 372, 383, 400]

#below for filling up backend with frames
def pick_and_save_frame():
    for index, row in enumerate(SQS_df.iterrows()):
        uas = row[1]['input.frames'].split(',')
        frame_list = [ua[2:].lower() for ua in uas]
        for frame in frame_list:
            fs = fn.frames('(?i)'+frame)
            for f in fs:
                if frame == f.name.lower():
                    if Frame.objects.filter(frame_name=frame).count()==0:
                        #print(index)
                        #print(f.URL)
                        try:
                            data = urlopen(f.URL)

                        except urllib.error.HTTPError:
                            print("Error on "+str(index))
                            continue
                        data = xmltodict.parse(data)
                        new_frame = Frame(frame_name=frame, frame_definition = data['frame']['definition'])
                        new_frame.save()
    return frame

def initialize_frame_sentences():
    Frame_Sentence.objects.all().delete()
    for index, row in enumerate(SQS_df.iterrows()):
        if index not in exclude_list:
            fs = Frame_Sentence(sentence_id = index)
            fs.save()
            if Frame_Sentence.objects.all().count() == 11:
                break

#to generate frame tasks when a worker comes in initially
def frame_checkbox_initialize_worker(wid, aid):
    init_sentence = Frame_Sentence.objects.get(sentence_id = INITIAL_TASK_SENTENCE)
    ft = Frame_Task(frame_sentence = init_sentence, wid=wid, aid=aid, task_sub_id=0)
    ft.save()
    for i in range(1, TOTAL_SUB_TASK_NUM):
        excludable = Frame_Task.objects.filter(wid=wid)
        taskable_sentence = Frame_Sentence.objects.exclude(frame_task__in = excludable)
        taskable_sentence = taskable_sentence.annotate(num_task=Count('frame_task')).filter(num_task__lt=TARGET_TASK_NUM)
        min_ = taskable_sentence.aggregate(min_num_task=Min('num_task'))
        min_num_task = min_['min_num_task']
        print(min_)
        taskable_sentence = taskable_sentence.filter(num_task = min_num_task)
        if taskable_sentence.count()==0:
            Frame_Task.objects.filter(wid=wid, aid=aid).delete()
            return False
        sentence = taskable_sentence[random.randint(0, taskable_sentence.count()-1)]
        ft = Frame_Task(frame_sentence = sentence, wid=wid, aid=aid, task_sub_id=i)
        ft.save()
    return True

#to get frames from the database
def get_frame_from_database(index):
    row = SQS_df.loc[int(index)]
    uas = row['input.frames'].split(',')
    frame_list = [ua[2:].lower() for ua in uas]
    frame_definitions = {}
    for frame in frame_list:
        fs = fn.frames('(?i)'+frame)
        for f in fs:
            if frame == f.name.lower():
                frame_definitions[frame] = Frame.objects.filter(frame_name = frame)[0].frame_definition#f.definition
    frame = {
        'target_sentence' : row['input.sentence'],
        'target_word' : row['input.word_phrase'],
        'frame_definitions' : frame_definitions,
    }
    return frame

def pick_and_get_frame_disambiguation_material(index, all_frames = False):
    row = SQS_df.loc[int(index)]
    if not all_frames:
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
        frame_list = [ua[2:].lower() for ua in uas]


    frame_definitions = {}
    for frame in frame_list:
        fs = fn.frames('(?i)'+frame)
        for f in fs:
            if frame == f.name.lower():
                data = urlopen(f.URL)
                #data = file.read()
                #file.close()
                data = xmltodict.parse(data)
                frame_definitions[frame] = data['frame']['definition']#f.definition
    frame = {
        'target_sentence' : row['input.sentence'],
        'target_word' : row['input.word_phrase'],
        'frame_definitions' : frame_definitions,
    }
    return frame
