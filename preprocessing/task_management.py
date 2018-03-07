from .models import *
from django.db.models import Count, F, ExpressionWrapper, DateTimeField
import uuid
import datetime
import json
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
def isp_store_result(result):
    criteria = result['criteria']
    batch_id = result['batch_id']
    task_results = result['task_result']
    #get items with same batch id
    if criteria == "video_quality":
        vote_batch = Video_quality_inspection_vote.objects.filter(batch_id = batch_id)
    elif criteria == "sound_quality":
        vote_batch = Sound_quality_inspection_vote.objects.filter(batch_id = batch_id)
    elif criteria == "language":
        vote_batch = Language_inspection_vote.objects.filter(batch_id = batch_id)
    elif criteria == "conversation":
        vote_batch = Conversation_inspection_vote.objects.filter(batch_id = batch_id)
    elif criteria == "scene":
        vote_batch = Scene_inspection_vote.objects.filter(batch_id = batch_id)

    for task_result in task_results:
        subject_video = Video.objects.filter(video_url = task_result)
        if subject_video.count()>0:
            #store batch data
            subject_video = subject_video[0]
            single_vote = vote_batch.filter(video = subject_video)
            if single_vote.count()>0:
                single_vote = single_vote[0]
                single_vote.end_time = datetime.datetime.now()
            else:
                if criteria == "video_quality":
                    single_vote = Video_quality_inspection_vote(video = subject_video, end_time = datetime.datetime.now()+datetime.timedelta(minutes = 10), batch_id = batch_id)
                elif criteria == "sound_quality":
                    single_vote = Sound_quality_inspection_vote(video = subject_video, end_time = datetime.datetime.now()+datetime.timedelta(minutes = 10), batch_id = batch_id)
                elif criteria == "language":
                    single_vote = Language_inspection_vote(video = subject_video, end_time = datetime.datetime.now()+datetime.timedelta(minutes = 10), batch_id = batch_id)
                elif criteria == "conversation":
                    single_vote = Conversation_inspection_vote(video = subject_video, end_time = datetime.datetime.now()+datetime.timedelta(minutes = 10), batch_id = batch_id)
                elif criteria == "scene":
                    single_vote = Scene_inspection_vote(video = subject_video, end_time = datetime.datetime.now()+datetime.timedelta(minutes = 10), batch_id = batch_id)
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



# this function select the field to deploy the tasks
def isp_select_field():
    # first get videos not fully inspected yet
    not_inspected = Video.objects.filter(fully_inspected = False)

    # filter videos whose scene is not checked
    scene_to_check = not_inspected.filter(sound_quality_passed = True, video_quality_passed = True, language_passed = True, conversation_passed = True)
    scene_not_to_check = not_inspected.exclude(sound_quality_passed = True, video_quality_passed = True, language_passed = True, conversation_passed = True)

        # among scene to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    scene_task_deployable = scene_to_check.annotate(number_of_deployed_tasks = Count('scene_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    if scene_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = scene_task_deployable.order_by('number_of_deployed_tasks')[:batch_number]
        return isp_generate_votes_and_throw_tasks(tasks_to_deploy, 'scene')


    # filter videos whose sound quality is not checked
    sound_to_check = scene_not_to_check.filter(video_quality_passed = True, language_passed = True, conversation_passed = True)
    sound_not_to_check = scene_not_to_check.exclude(video_quality_passed = True, language_passed = True, conversation_passed = True)

        # among sound to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    sound_task_deployable = sound_to_check.annotate(number_of_deployed_tasks = Count('sound_quality_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    if sound_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = sound_task_deployable.order_by('number_of_deployed_tasks')[:batch_number]
        return isp_generate_votes_and_throw_tasks(tasks_to_deploy, 'sound_quality')


    # filter videos whose video quality is not checked
    video_to_check = sound_not_to_check.filter(language_passed = True, conversation_passed = True)
    video_not_to_check = sound_not_to_check.exclude(language_passed = True, conversation_passed = True)

        # among video to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    video_task_deployable = video_to_check.annotate(number_of_deployed_tasks = Count('video_quality_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    if video_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = video_task_deployable.order_by('number_of_deployed_tasks')[:batch_number]
        return isp_generate_votes_and_throw_tasks(tasks_to_deploy, 'video_quality')


    # filter videos whose language is not checked
    language_to_check = video_not_to_check.filter(conversation_passed = True)

        # among language to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    language_task_deployable = language_to_check.annotate(number_of_deployed_tasks = Count('language_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    if language_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = language_task_deployable.order_by('number_of_deployed_tasks')[:batch_number]
        return isp_generate_votes_and_throw_tasks(tasks_to_deploy, 'language')

    # for the rest, conversation can be checked
    conversation_to_check = video_not_to_check.exclude(conversation_passed = True)

        # among language to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    conversation_task_deployable = conversation_to_check.annotate(number_of_deployed_tasks = Count('conversation_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    if conversation_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = conversation_task_deployable.order_by('number_of_deployed_tasks')[:batch_number]
        return isp_generate_votes_and_throw_tasks(tasks_to_deploy, 'conversation')

# this function generates vote entities and throw tasks as lists of urls
def isp_generate_votes_and_throw_tasks(tasks_to_deploy, vote_type):
    batch_id = str(uuid.uuid4().hex.upper()[0:6])
    task_series = []
    for task in tasks_to_deploy:
        if vote_type=='conversation':
            vote = Conversation_inspection_vote(video = task, batch_id = batch_id)
        elif vote_type=='language':
            vote = Language_inspection_vote(video = task, batch_id = batch_id)
        elif vote_type=='video_quality':
            vote = Video_quality_inspection_vote(video = task, batch_id = batch_id)
        elif vote_type=='sound_quality':
            vote = Sound_quality_inspection_vote(video = task, batch_id = batch_id)
        elif vote_type=='scene':
            vote = Scene_quality_inspection_vote(video = task, batch_id = batch_id)
        vote.save()
        task_series.append(task.video_url)
    return_dict = {
        'batch_number': batch_number,
        'batch_id' : batch_id,
        'criteria' : vote_type,
        'task_series' : json.dumps(task_series),
    }

    return return_dict