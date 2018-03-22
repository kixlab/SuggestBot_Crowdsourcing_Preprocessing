from .models import *
from django.db.models import Count, F, ExpressionWrapper, DateTimeField
import uuid
import datetime
import json
import random
# When building the backend, task should be assigned based on video numbers.folder.
# For example, if there are 10 videos that need face grouping,
# each worker should access one video folder and download all median bounding box
# images to start the grouping.
# Once the groupling is done, a json file with the grouping info can be sent back
# to the folder containing the median image.
# Once the system hits 10th video, or the latest video, it can come back to the
# first video and check if there is a json file in the folder.
# If no json file, assign a worker to do the grouping task.

#below is the number of videos given to single worker
batch_number = 5

#below is the number of votes for each tasks
vote_number = 3

# TODO function to receive results and update as 'done' (change time)
# This function is copy pasted from task_management.py,
# and has to be rewritten
def fbg_store_result(result, wid, aid):
    criteria = result['criteria']
    batch_id = result['batch_id']
    task_results = result['task_result']

    token = str(uuid.uuid4().hex.upper()[0:6])
    tokeninfo = TokenInfo(token = token, wid = wid, aid = aid)
    tokeninfo.save()
    #get items with same batch id
    if criteria == "video_quality":
        vote_batch = Video_quality_inspection_vote.objects.filter(batch_id = batch_id, w_id = wid)
    elif criteria == "sound_quality":
        vote_batch = Sound_quality_inspection_vote.objects.filter(batch_id = batch_id, w_id = wid)
    elif criteria == "language":
        vote_batch = Language_inspection_vote.objects.filter(batch_id = batch_id, w_id = wid)
    elif criteria == "conversation":
        vote_batch = Conversation_inspection_vote.objects.filter(batch_id = batch_id, w_id = wid)
    elif criteria == "scene":
        vote_batch = Scene_inspection_vote.objects.filter(batch_id = batch_id, w_id = wid)

    for task_result in task_results:
        subject_video = Video.objects.filter(video_url = task_result)
        print(subject_video)
        if subject_video.count()>0:
            #store batch data
            subject_video = subject_video[0]
            single_vote = vote_batch.filter(video = subject_video)
            if single_vote.count()>0:
                single_vote = single_vote[0]
                single_vote.end_time = datetime.datetime.now()
            else:
                if criteria == "video_quality":
                    single_vote = Video_quality_inspection_vote(video = subject_video, end_time = datetime.datetime.now()+datetime.timedelta(minutes = 10), batch_id = batch_id, w_id = wid)
                elif criteria == "sound_quality":
                    single_vote = Sound_quality_inspection_vote(video = subject_video, end_time = datetime.datetime.now()+datetime.timedelta(minutes = 10), batch_id = batch_id, w_id = wid)
                elif criteria == "language":
                    single_vote = Language_inspection_vote(video = subject_video, end_time = datetime.datetime.now()+datetime.timedelta(minutes = 10), batch_id = batch_id, w_id = wid)
                elif criteria == "conversation":
                    single_vote = Conversation_inspection_vote(video = subject_video, end_time = datetime.datetime.now()+datetime.timedelta(minutes = 10), batch_id = batch_id, w_id = wid)
                elif criteria == "scene":
                    single_vote = Scene_inspection_vote(video = subject_video, end_time = datetime.datetime.now()+datetime.timedelta(minutes = 10), batch_id = batch_id, w_id = wid)
            single_vote.qualified = task_results[task_result]
            single_vote.save()
            #if stored batch data, then see if vote_number of votes are collected
            if criteria == "video_quality":
                accumulated_votes = Video_quality_inspection_vote.objects.filter(video = subject_video)
            elif criteria == "sound_quality":
                accumulated_votes = Sound_quality_inspection_vote.objects.filter(video = subject_video)
            elif criteria == "language":
                accumulated_votes = Language_inspection_vote.objects.filter(video = subject_video)
            elif criteria == "conversation":
                accumulated_votes = Conversation_inspection_vote.objects.filter(video = subject_video)
            elif criteria == "scene":
                accumulated_votes = Scene_inspection_vote.objects.filter(video = subject_video)
            accumulated_votes_count = accumulated_votes.count()
            if accumulated_votes_count >=vote_number:
                #if so, mark the result
                qualified_count = accumulated_votes.filter(qualified = True).count()
                non_qualified_count = accumulated_votes_count - qualified_count
                if qualified_count >= non_qualified_count :
                    qualification_result = True
                else:
                    qualification_result = False
                if criteria == "video_quality":
                    if qualification_result:
                        subject_video.video_quality_passed = True
                    else:
                        subject_video.fully_inspected = True
                elif criteria == "sound_quality":
                    if qualification_result:
                        subject_video.sound_quality_passed = True
                    else:
                        subject_video.fully_inspected = True
                elif criteria == "language":
                    if qualification_result:
                        subject_video.language_passed = True
                    else:
                        subject_video.fully_inspected = True
                elif criteria == "conversation":
                    if qualification_result:
                        subject_video.conversation_passed = True
                    else:
                        subject_video.fully_inspected = True
                elif criteria == "scene":
                    if qualification_result:
                        subject_video.scene_passed = True
                        subject_video.fully_inspected = True
                    else:
                        subject_video.fully_inspected = True
                subject_video.save()
    return token

def fbg_deployer():
    videos = Video.objects.all()[:batch_number]
    task_series = []
    for video in videos:
        task_series.append(video.video_url)
    return_dict = {
        'batch_number': batch_number,
        'batch_id': batch_id,
        'criteria': criteria,
        'task_series': json.dumps(task_series),
    }
    return return_dict

# this function generates vote entities and throw tasks as lists of urls
def isp_generate_votes_and_throw_tasks(wid, aid, tasks_to_deploy, vote_type):
    task_series = []
    for task in tasks_to_deploy:
        if vote_type=='conversation':
            vote = Conversation_inspection_vote(video = task, batch_id = aid, w_id = wid)
        elif vote_type=='language':
            vote = Language_inspection_vote(video = task, batch_id = aid, w_id = wid)
        elif vote_type=='video_quality':
            vote = Video_quality_inspection_vote(video = task, batch_id = aid, w_id = wid)
        elif vote_type=='sound_quality':
            vote = Sound_quality_inspection_vote(video = task, batch_id = aid, w_id = wid)
        elif vote_type=='scene':
            vote = Scene_inspection_vote(video = task, batch_id = aid, w_id = wid)
        vote.save()
        task_series.append(task.video_url)
    return_dict = {
        'batch_number': batch_number,
        'batch_id' : aid,
        'criteria' : vote_type,
        'task_series' : json.dumps(task_series),
    }

    return return_dict
