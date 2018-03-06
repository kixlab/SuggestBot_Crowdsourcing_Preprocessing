from .models import *
from django.db.models import Count
import uuid
# task will be assigned based on current status of whole available works
# in the order of
# conversation -> language -> visual quality -> audio quality -> scene
# if every fields are filled, it will marked as fully inspected

#below is the number of videos given to single worker
batch_number = 5

#below is the number of votes for each tasks
vote_number = 3

# TODO function to remove any outdated tasks
def remove_outdated_tasks():
    return

# TODO function to receive results and update as 'done' (change time)

# this function select the field to deploy the tasks
def select_field():
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
        generate_votes_and_throw_tasks(tasks_to_deploy, 'scene')
        return

    # filter videos whose sound quality is not checked
    sound_to_check = scene_not_to_check.filter(video_quality_passed = True, language_passed = True, conversation_passed = True)
    sound_not_to_check = scene_not_to_check.exclude(video_quality_passed = True, language_passed = True, conversation_passed = True)

        # among sound to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    sound_task_deployable = sound_to_check.annotate(number_of_deployed_tasks = Count('sound_quality_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    if sound_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = sound_task_deployable.order_by('number_of_deployed_tasks')[:batch_number]
        generate_votes_and_throw_tasks(tasks_to_deploy, 'sound_quality')
        return

    # filter videos whose video quality is not checked
    video_to_check = sound_not_to_check.filter(language_passed = True, conversation_passed = True)
    video_not_to_check = sound_not_to_check.exclude(language_passed = True, conversation_passed = True)

        # among video to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    video_task_deployable = video_to_check.annotate(number_of_deployed_tasks = Count('video_quality_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    if video_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = video_task_deployable.order_by('number_of_deployed_tasks')[:batch_number]
        generate_votes_and_throw_tasks(tasks_to_deploy, 'video_quality')
        return

    # filter videos whose language is not checked
    language_to_check = video_not_to_check.filter(conversation_passed = True)

        # among language to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    language_task_deployable = language_to_check.annotate(number_of_deployed_tasks = Count('language_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    if language_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = language_task_deployable.order_by('number_of_deployed_tasks')[:batch_number]
        generate_votes_and_throw_tasks(tasks_to_deploy, 'language')
        return

    # for the rest, conversation can be checked
    conversation_to_check = video_not_to_check.exclude(conversation_passed = True)

        # among language to check see if there are more than batch_number of tasks to do
        # (= deployed number of tasks should be less than vote number)
    conversation_task_deployable = conversation_to_check.annotate(number_of_deployed_tasks = Count('conversation_inspection_vote')).filter(number_of_deployed_tasks__lt = vote_number)
    if conversation_task_deployable.count() >= batch_number:
        # deploy task
        tasks_to_deploy = conversation_task_deployable.order_by('number_of_deployed_tasks')[:batch_number]
        generate_votes_and_throw_tasks(tasks_to_deploy, 'conversation')
        return

# this function generates vote entities and throw tasks as lists of urls
def generate_votes_and_throw_tasks(tasks_to_deploy, vote_type):
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
    print(task_series)
