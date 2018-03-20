from .models import *
from django.db.models import Count, F, ExpressionWrapper, DateTimeField
import uuid
import datetime
import json
import random
# task will be assigned based on current status of whole available works
# in the order of
# conversation -> language -> visual quality -> audio quality -> scene
# if every fields are filled, it will marked as fully inspected

#below is the number of videos given to single worker
batch_number = 5

#below is the number of votes for each tasks
vote_number = 3

TASK_TIME_LIMIT = 5

# TODO function to remove any outdated tasks
def isp_remove_outdated_tasks():
    # ***BE CAUTIOUS***
    # Below code utilized systematic characteristic of start time being generated a bit later than end time (in microseconds).
    # If systematic characteristic changes, the below code might not work
    conv=Conversation_inspection_vote.objects.filter(start_time__gte = F('end_time'), start_time__lte = datetime.datetime.now()-datetime.timedelta(minutes=TASK_TIME_LIMIT))
    lang=Language_inspection_vote.objects.filter(start_time__gte = F('end_time'), start_time__lte = datetime.datetime.now()-datetime.timedelta(minutes=TASK_TIME_LIMIT))
    video=Video_quality_inspection_vote.objects.filter(start_time__gte = F('end_time'), start_time__lte = datetime.datetime.now()-datetime.timedelta(minutes=TASK_TIME_LIMIT))
    sound=Sound_quality_inspection_vote.objects.filter(start_time__gte = F('end_time'), start_time__lte = datetime.datetime.now()-datetime.timedelta(minutes=TASK_TIME_LIMIT))
    scene=Scene_inspection_vote.objects.filter(start_time__gte = F('end_time'), start_time__lte = datetime.datetime.now()-datetime.timedelta(minutes=TASK_TIME_LIMIT))

    conv.delete()
    lang.delete()
    video.delete()
    sound.delete()
    scene.delete()
    return

# TODO function to receive results and update as 'done' (change time)
def isp_store_result(result, wid, aid):
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


# this function select the field to deploy the tasks
def isp_select_field(wid, aid):
    # first get videos not fully inspected yet
    not_inspected = Video.objects.filter(fully_inspected = False)
    print(not_inspected)
    # filter videos whose scene is not checked
    scene_to_check = not_inspected.filter(sound_quality_passed = True, video_quality_passed = True, language_passed = True, conversation_passed = True)
    scene_not_to_check = not_inspected.exclude(sound_quality_passed = True, video_quality_passed = True, language_passed = True, conversation_passed = True)

        # among scene to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    scene_task_deployable = scene_to_check.annotate(number_of_deployed_tasks = Count('scene_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    scene_task_deployable = scene_task_deployable.exclude(scene_inspection_vote__w_id=wid)
    if scene_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = scene_task_deployable[:batch_number]
        return isp_generate_votes_and_throw_tasks(wid, aid, tasks_to_deploy, 'scene')


    # filter videos whose sound quality is not checked
    sound_to_check = scene_not_to_check.filter(video_quality_passed = True, language_passed = True, conversation_passed = True)
    sound_not_to_check = scene_not_to_check.exclude(video_quality_passed = True, language_passed = True, conversation_passed = True)

        # among sound to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    sound_task_deployable = sound_to_check.annotate(number_of_deployed_tasks = Count('sound_quality_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    sound_task_deployable = sound_task_deployable.exclude(sound_quality_inspection_vote__w_id=wid)
    if sound_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = sound_task_deployable[:batch_number]
        return isp_generate_votes_and_throw_tasks(wid, aid, tasks_to_deploy, 'sound_quality')


    # filter videos whose video quality is not checked
    video_to_check = sound_not_to_check.filter(language_passed = True, conversation_passed = True)
    video_not_to_check = sound_not_to_check.exclude(language_passed = True, conversation_passed = True)

        # among video to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    video_task_deployable = video_to_check.annotate(number_of_deployed_tasks = Count('video_quality_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    video_task_deployable = video_task_deployable.exclude(video_quality_inspection_vote__w_id=wid)
    if video_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = video_task_deployable[:batch_number]
        return isp_generate_votes_and_throw_tasks(wid, aid, tasks_to_deploy, 'video_quality')


    # filter videos whose language is not checked
    language_to_check = video_not_to_check.filter(conversation_passed = True)

        # among language to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    language_task_deployable = language_to_check.annotate(number_of_deployed_tasks = Count('language_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    print(language_task_deployable)
    language_task_deployable = language_task_deployable.exclude(language_inspection_vote__w_id=wid)
    print(language_task_deployable)
    if language_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = language_task_deployable[:batch_number]
        return isp_generate_votes_and_throw_tasks(wid, aid, tasks_to_deploy, 'language')

    # for the rest, conversation can be checked
    conversation_to_check = video_not_to_check.exclude(conversation_passed = True)

        # among language to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    conversation_task_deployable = conversation_to_check.annotate(number_of_deployed_tasks = Count('conversation_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    conversation_task_deployable = conversation_task_deployable.exclude(conversation_inspection_vote__w_id=wid)
    if conversation_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = conversation_task_deployable[:batch_number]
        return isp_generate_votes_and_throw_tasks(wid, aid, tasks_to_deploy, 'conversation')

def test_deployer():
    randomnum = random.uniform(0,1)
    print(randomnum)
    batch_id = "test"
    if randomnum >=0 and randomnum <0.2:
        criteria = "conversation"
    elif randomnum >=0.2 and randomnum <0.4:
        criteria = "language"
    elif randomnum >=0.4 and randomnum <0.6:
        criteria = "video_quality"
    elif randomnum >=0.6 and randomnum <0.8:
        criteria = "sound_quality"
    elif randomnum >=0.8 and randomnum <=1:
        criteria = "scene"
    videos = Video.objects.all()[:batch_number]
    task_series = []
    for video in videos:
        task_series.append(video.video_url)
    return_dict = {
        'batch_number': batch_number,
        'batch_id': batch_id,
        'criteria': criteria,
        'task_series': json.dumps(task_series),
        'debug' : 1,
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
        'debug' : 0,
    }

    return return_dict
