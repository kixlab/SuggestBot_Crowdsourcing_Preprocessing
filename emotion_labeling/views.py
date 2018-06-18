from django.shortcuts import render, redirect, reverse
import json
from django.http import HttpResponse, JsonResponse
from .forms import *
from .models import *
from .emotion_label_management import *
import uuid
from boto.mturk.connection import MTurkConnection
from boto.mturk.price import Price
import base64
from .character_time_designate import *
from .mturk_task_management import Create_Emotion_Distribution_collection_HIT, date_handler
from django.db.models import Q
from .MTURKKEY import *
from .emotion_distribution_management import *
from .frame_disambiguation_filter import *
import datetime
# Create your views here.

def study_frame_checkbox_confidence(request, wid, aid, task_num):
    print(wid)
    #initialize_frame_sentences()
    #TODO delete deprecated task items - all the tasks by none-paid workers should be deleted!
    ft_to_deletes = Frame_Task.objects.filter(start_time__gte = F('end_time'), start_time__lte = datetime.datetime.now()-datetime.timedelta(minutes=TASK_TIME_LIMIT))
    for ft_to_delete in ft_to_deletes:
        Frame_Task.objects.filter(wid = ft_to_delete.wid, aid = ft_to_delete.aid).delete()

    if request.method=="POST":
        #TODOdone...? save items
        #TODOdone...? update Frame Task
        form = FrameStudyResult(request.POST)
        frame_task = Frame_Task.objects.get(task_sub_id = int(task_num) ,wid=wid, aid=aid)
        frame_task.end_time = datetime.datetime.now()
        print(form)
        print(type(form.cleaned_data['frame_confidences']))
        frame_task.frame_confidences = form.cleaned_data['frame_confidences']
        frame_task.no_field_reasoning = form.cleaned_data['no_field_reasoning']
        frame_task.save()
        if int(task_num)!=TOTAL_SUB_TASK_NUM-1:
            return redirect('/emotion_labeling/study_frame_checkbox_confidence/'+wid+'/'+aid+'/'+str(int(task_num)+1))
        else:
            token = {'token': 'test_token'}
            return render(request, "token_return.html", token)
    if int(task_num) == 0:
        #TODOdone...? generate 6 Frame_Task items including sanity check
        taskable = frame_checkbox_initialize_worker(wid, aid)
        frame = get_frame_from_database(INITIAL_TASK_SENTENCE)
        if not taskable:
            return HttpResponse("Sorry, you have done all the task you can do, or there is no more of available task.")
    else:
        #TODOdone..? get the frame sentence number from previously generated taks
        target_sentence = Frame_Task.objects.filter(wid=wid, aid=aid, task_sub_id=int(task_num))[0].frame_sentence.sentence_id
        frame = get_frame_from_database(target_sentence)

    to_send = {
        'task_num' :task_num,
        'frame' : frame,
    }
    return render(request, "study_frame_checkbox_confidence.html", to_send)

def interface_study_arousal_valence(request, data_name):
    study_video = Study_Video.objects.get(video_title = data_name)
    to_send = {
        'natural_language_instruction' : "Express how you would interpret the emotion of the character in terms of arousal and valence in natural language.",
        'subject_data_name' : 'the emotion of the character',
        'classes' : json.dumps([]),
        'label_complexity': '2d-scale',
        'condition': 'study_arousal_valence',
        'max_tuto': 6,
        'target_second': study_video.video_prompt_time,
        'target_img': study_video.video_img,
        'source': study_video.video_url,
    }
    return render(request, "interface_study_video.html", to_send)

def interface_study_emotion_word(request, data_name):
    to_send = {
        'source' : "https://firebasestorage.googleapis.com/v0/b/suggestbot-preprocessing.appspot.com/o/A%20Man%20Like%20You%20%20%20%20A%20Short%20Film%20from%20Harry%E2%80%99s.mp4?alt=media&token=8f79cbc2-ca80-498e-a262",
        'natural_language_instruction' : "Express how you would interpret the emotion of the character in terms of the emotion word in natural language.",
        'subject_data_name' : 'the emotion of the character',
        'classes' : json.dumps(['joyful', 'sad', 'angry', 'disgusted', 'fearful', 'surprised', 'neutral']),
        'label_complexity': 'multiclass',
        'condition': 'study_emotion_word',
        'max_tuto': 1,
    }
    return render(request, "interface_study_video.html", to_send)

def interface_study_frame_disambiguation(request, data_name):
    frame = pick_and_get_frame_disambiguation_material(data_name)
    to_send = {
        'natural_language_instruction' : "Express how you would interpret the possible meaning of the word in terms of given frame classes in natural language.",
        'subject_data_name' : 'the frame of the word',
        'classes' : json.dumps(['a', 'b', 'c', 'd', 'e', 'f', 'g']),
        'label_complexity': 'multiclass',
        'frame' : frame,
    }
    return render(request, "interface_study_text.html", to_send)

def interface_study_student_engagement(request, data_name):
    to_send = {
        'natural_language_instruction' : "Express how you would interpret the possible meaning of the word in terms of given frame classes in natural language.",
        'subject_data_name' : 'the frame of the word',
        'classes' : json.dumps(['a', 'b', 'c', 'd', 'e', 'f', 'g']),
        'label_complexity': 'scale',
    }
    return render(request, "interface_study_image.html", to_send)

# pick a single point label
def experiment1_baseline(request, video_title, wid, aid):
    exp_video = Experiment_Video.objects.filter(video_title = video_title)[0]
    if request.method=="POST":
        form = EmotionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])
        #TODO change saving function
        token = Experiment_Label_Baseline_Store(exp_video, to_return, wid, aid)
        token = {'token': token}
        return render(request, "token_return.html", token)

    prompt_time = json.loads(exp_video.video_prompt_time)
    print(prompt_time)

    task_to_throw = {
    # which video?
        'video_title': exp_video.video_title,
        'video_url': exp_video.video_url,
        'video_img': exp_video.video_img,
    # in which condition?  --> condition should be 'experiment_reasoning' or 'experiment_baseline'
        'condition': 'experiment_baseline',
    # in which time do the system prompts?
        'prompt_time': exp_video.video_prompt_time,
    # additional info that is sent for sanity check
        'label_to_check': json.dumps({}),
    }
    # *** for images, you should store them in '/static/img/figures/{{condition}}/{{video_url}}/{{video_url}}{{character}}'
    # based on the condition, url will be differently assigned

    return render(request, "emotion_labeling_baseline.html", task_to_throw)

# generate a distributional label - baseline
def experiment1_distribution(request, video_title, wid, aid):
    exp_video = Experiment_Video.objects.filter(video_title = video_title)[0]
    if request.method=="POST":
        form = DistributionResult(request.POST)
        print(form)
        start_time = form.cleaned_data['start_time']
        to_return = json.loads(form.cleaned_data['to_return'])
        print(to_return)
        print(start_time)
        #TODO change saving function
        token = Experiment_Distribution_Store(exp_video, to_return, start_time, wid, aid)
        token = {'token': token}
        return render(request, "token_return.html", token)

    prompt_time = json.loads(exp_video.video_prompt_time)
    print(prompt_time)

    task_to_throw = {
    # which video?
        'video_title': exp_video.video_title,
        'video_url': exp_video.video_url,
        'video_img': exp_video.video_img,
    # in which condition?  --> condition should be 'experiment_reasoning' or 'experiment_baseline'
        'condition': 'experiment_distribution',
    # in which time do the system prompts?
        'prompt_time': exp_video.video_prompt_time,
    # additional info that is sent for sanity check
        'label_to_check': json.dumps({}),
    }
    # *** for images, you should store them in '/static/img/figures/{{condition}}/{{video_url}}/{{video_url}}{{character}}'
    # based on the condition, url will be differently assigned

    return render(request, "emotion_labeling_distribution.html", task_to_throw)

# tutorial for tutorial-like example - show both example and distribution_input
def experiment1_distribution_tutolike_ED_tutorial(request, video_title, wid, aid):
    exp_video = Experiment_Video.objects.filter(video_title = video_title)[0]
    if request.method=="POST":
        # test
        #if request.POST['expression']=='3' and request.POST['event']=='1':
            #mtc.grant_bonus(wid, aid, Price(4.00), "You passed prescreen, so you get this bonus!")
        return redirect('/emotion_labeling/experiment1_distribution_tutolike_ED/'+video_title+'/'+wid+'/'+aid)
        #else:
        #    token = {'token': str(uuid.uuid4().hex.upper()[0:6])}
        #    return render(request, "prescreen_fail_token_return.html", token)
    time_work = {
        'video_total_time': exp_video.video_total_time,
        'video_prompt_num': exp_video.video_prompt_num,
        'condition': 'tutolike_ED'
    }
    time_work = extract_representative_examples(time_work)
    return render(request, 'emotion_labeling_distribution_tutolike_ED_tutorial.html',time_work)

def experiment1_distribution_tutolike_ED(request, video_title, wid, aid):
    exp_video = Experiment_Video.objects.filter(video_title = video_title)[0]
    if request.method=="POST":
        form = EmotionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])
        #TODO change saving function
        #token = Experiment_Label_Baseline_Store(exp_video, to_return, wid, aid)
        token = {'token': token}
        return render(request, "token_return.html", token)

    prompt_time = json.loads(exp_video.video_prompt_time)
    print(prompt_time)

    task_to_throw = {
    # which video?
        'video_title': exp_video.video_title,
        'video_url': exp_video.video_url,
        'video_img': exp_video.video_img,
    # in which condition?  --> condition should be 'experiment_reasoning' or 'experiment_baseline'
        'condition': 'experiment_baseline',
    # in which time do the system prompts?
        'prompt_time': exp_video.video_prompt_time,
    # additional info that is sent for sanity check
        'label_to_check': json.dumps({}),
    }
    # *** for images, you should store them in '/static/img/figures/{{condition}}/{{video_url}}/{{video_url}}{{character}}'
    # based on the condition, url will be differently assigned

    #below assigns examples
    task_to_throw = extract_representative_examples(task_to_throw)
    return render(request, "emotion_labeling_distribution_tutolike_ED.html", task_to_throw)

def experiment1_distribution_adaptive_ED(request, video_title, wid, aid):
    exp_video = Experiment_Video.objects.filter(video_title = video_title)[0]
    if request.method=="POST":
        form = EmotionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])
        #TODO change saving function
        #token = Experiment_Label_Baseline_Store(exp_video, to_return, wid, aid)
        token = {'token': token}
        return render(request, "token_return.html", token)

    prompt_time = json.loads(exp_video.video_prompt_time)
    print(prompt_time)

    task_to_throw = {
    # which video?
        'video_title': exp_video.video_title,
        'video_url': exp_video.video_url,
        'video_img': exp_video.video_img,
    # in which condition?  --> condition should be 'experiment_reasoning' or 'experiment_baseline'
        'condition': 'experiment_baseline',
    # in which time do the system prompts?
        'prompt_time': exp_video.video_prompt_time,
    # additional info that is sent for sanity check
        'label_to_check': json.dumps({}),
    }
    # *** for images, you should store them in '/static/img/figures/{{condition}}/{{video_url}}/{{video_url}}{{character}}'
    # based on the condition, url will be differently assigned

    return render(request, "emotion_labeling_distribution_adaptive_ED.html", task_to_throw)

def experiment1_cp(request, video_title, wid, aid):
    exp_video = Experiment_Video.objects.filter(video_title = video_title)[0]
    if request.method=="POST":
        form = EmotionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])
        token = Experiment_Label_Component_Process_Store(exp_video, to_return, wid, aid)
        token = {'token': token}
        return render(request, "token_return.html", token)

    prompt_time = json.loads(exp_video.video_prompt_time)
    print(prompt_time)

    task_to_throw = {
    # which video?
        'video_title': exp_video.video_title,
        'video_url': exp_video.video_url,
        'video_img': exp_video.video_img,
    # in which condition?  --> condition should be 'experiment_reasoning' or 'experiment_baseline'
        'condition': 'experiment_reasoning',
    # in which time do the system prompts?
        'prompt_time': exp_video.video_prompt_time,
    # additional info that is sent for sanity check
        'label_to_check': json.dumps({}),
        'step': "label_and_reason",
    }
    # *** for images, you should store them in '/static/img/figures/{{condition}}/{{video_url}}/{{video_url}}{{character}}'
    # based on the condition, url will be differently assigned

    return render(request, "emotion_labeling_component_process.html", task_to_throw)
# component process tutorial
def experiment1_cp_prescreening(request, video_title, wid, aid):
    exp_video = Experiment_Video.objects.filter(video_title = video_title)[0]
    if request.method=="POST":
        # test
        #if request.POST['expression']=='3' and request.POST['event']=='1':
            #mtc.grant_bonus(wid, aid, Price(4.00), "You passed prescreen, so you get this bonus!")
        return redirect('/emotion_labeling/experiment1_cp_likert/'+video_title+'/'+wid+'/'+aid)
        #else:
        #    token = {'token': str(uuid.uuid4().hex.upper()[0:6])}
        #    return render(request, "prescreen_fail_token_return.html", token)
    time_work = {
        'video_total_time': exp_video.video_total_time,
        'video_prompt_num': exp_video.video_prompt_num,
    }
    return render(request, 'emotion_labeling_component_process_prescreening.html',time_work)
# component process
def experiment1_cp_likert(request, video_title, wid, aid):
    exp_video = Experiment_Video.objects.filter(video_title = video_title)[0]
    if request.method=="POST":
        form = EmotionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])
        token = Experiment_Label_Component_Process_Store_Likert(exp_video, to_return, wid, aid)
        token = {'token': token}
        return render(request, "token_return.html", token)

    prompt_time = json.loads(exp_video.video_prompt_time)
    print(prompt_time)

    task_to_throw = {
    # which video?
        'video_title': exp_video.video_title,
        'video_url': exp_video.video_url,
        'video_img': exp_video.video_img,
    # in which condition?  --> condition should be 'experiment_reasoning' or 'experiment_baseline'
        'condition': 'experiment_reasoning',
    # in which time do the system prompts?
        'prompt_time': exp_video.video_prompt_time,
    # additional info that is sent for sanity check
        'label_to_check': json.dumps({}),
    }
    # *** for images, you should store them in '/static/img/figures/{{condition}}/{{video_url}}/{{video_url}}{{character}}'
    # based on the condition, url will be differently assigned

    return render(request, "emotion_labeling_component_process_likert.html", task_to_throw)

def experiment1_cp_only(request, video_title, wid, aid):
    exp_video = Experiment_Video.objects.filter(video_title = video_title)[0]
    if request.method=="POST":
        form = EmotionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])
        token = Experiment_Label_Component_Process_Store_Only(exp_video, to_return, wid, aid)
        token = {'token': token}
        return render(request, "token_return.html", token)

    prompt_time = json.loads(exp_video.video_prompt_time)
    print(prompt_time)

    task_to_throw = {
    # which video?
        'video_title': exp_video.video_title,
        'video_url': exp_video.video_url,
        'video_img': exp_video.video_img,
    # in which condition?  --> condition should be 'experiment_reasoning' or 'experiment_baseline'
        'condition': 'experiment_cp_only',
    # in which time do the system prompts?
        'prompt_time': exp_video.video_prompt_time,
    # additional info that is sent for sanity check
        'label_to_check': json.dumps({}),
    }
    # *** for images, you should store them in '/static/img/figures/{{condition}}/{{video_url}}/{{video_url}}{{character}}'
    # based on the condition, url will be differently assigned

    return render(request, "emotion_labeling_component_process_only.html", task_to_throw)



def character_time_designator(request, title):
    video = Video_Before_Processing.objects.filter(video_title = title)[0]
    if request.method=="POST":
        form = EmotionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])

        save_character_time_data(to_return, title, video.video_url)
        return HttpResponse("Successfully returned")


    task_to_throw ={
        'url': video.video_url,
    }
    return render(request, "character_time_designator.html", task_to_throw)
#decide task and deploy
def emotion_task_deploy_distribution(request, pass_word):
    if pass_word != PASS_WORD:
        return HttpResponse("Input appropriate password.")
    if request.method=="POST":
        form = TaskDeployResult(request.POST)
        print(form)
        hit_num = form.cleaned_data['hit_num']
        to_return = json.loads(form.cleaned_data['to_return'])
        for video_title in to_return:
            video = Experiment_Video.objects.filter(video_title = video_title)[0]
            hit = Create_Emotion_Distribution_collection_HIT(video_title, hit_num)
            video.video_hit_dict = json.dumps(hit, default=date_handler)
            video.save()
        return HttpResponse("Successfully Deployed")
    print(Experiment_Video.objects.filter(video_title="a_man_like_you0")[0].video_hit_dict)
    task_list = Experiment_Video.objects.filter(Q(video_hit_dict="")|Q(video_hit_dict=None))
    task_to_throw = {
        'task_list': task_list,
    }
    return render(request, "emotion_task_deploy.html", task_to_throw)

# run this function only once unless you will pay bonus multiple times for a worker
def bonus_for_hits(request, hit):
    passed_num =0
    assignments = mtc.get_assignments(hit)
    for a in assignments:
        label_count = Emotion_Label_Component_Process_Likert.objects.filter(wid = a.WorkerId, aid= a.AssignmentId).count()
        bonus = Bonus_Paid.objects.filter(wid=a.WorkerId, aid=a.AssignmentId, hid=hit).count()
        if label_count > 0 and bonus == 0:
            mtc.grant_bonus(a.WorkerId, a.AssignmentId, Price(4.00), "You passed prescreen, so you get this bonus!")
            nb = Bonus_Paid(wid=a.WorkerId, aid=AssignmentId, hid=hit)
            nb.save()
            # do accept also here?
            passed_num = passed_num+1
    return HttpResponse("Paid bonus to "+str(passed_num)+" workers")

### view for building example
def build_examples_from_collected_data(request):
    build_examples()
    return HttpResponse("Success")

### view for extracting similar examples
def extract_similar_examples(request):
    cur_dist = json.loads(request.GET.get("distribution"))
    print(cur_dist)
    examples = extract_example_from_preliminary_points(cur_dist)

    return JsonResponse(examples)
