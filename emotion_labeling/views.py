from django.shortcuts import render, redirect, reverse
import json
from django.http import HttpResponse
from .forms import *
from .models import *
from .emotion_label_management import *
import uuid
from boto.mturk.connection import MTurkConnection
from boto.mturk.price import Price
import base64
from .character_time_designate import *
# Create your views here.

#mtc = MTurkConnection(aws_access_key_id='fake', aws_secret_access_key='fake', host='mechanicalturk.sandbox.amazonaws.com')

def in_lab(request, video_title):
    print(request)
    worker_id = str(uuid.uuid4().hex.upper()[0:6])
    ass_id = str(uuid.uuid4().hex.upper()[0:6])
    return redirect('/emotion_labeling/experiment1/experiment_reasoning/'+video_title+'/'+worker_id+'/'+ass_id)#HttpResponse("<a >Click here to be redirected</a>")

def experiment1(request, condition, video_title, wid, aid):
    exp_video = Experiment_Video.objects.filter(video_title = video_title)[0]
    if request.method=="POST":
        form = EmotionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])
        token = Experiment_Label_Store(exp_video, to_return, wid, aid, condition)
        token = {'token': token}
        return render(request, "token_return.html", token)

    prompt_time = json.loads(exp_video.video_prompt_time)
    print(prompt_time)

    task_to_throw = {
    # which video?
        'video_title': exp_video.video_title,
        'video_url': exp_video.video_url,
    # which character?
        'character': "",
    # in which condition?  --> condition should be 'experiment_reasoning' or 'experiment_baseline'
        'condition': condition,
    # in which time do the system prompts?
        'prompt_time': exp_video.video_prompt_time,
    # additional info that is sent for sanity check
        'label_to_check': json.dumps({}),
        'step': "label_and_reason",
    }
    # *** for images, you should store them in '/static/img/figures/{{condition}}/{{video_url}}/{{video_url}}{{character}}'
    # based on the condition, url will be differently assigned

    return render(request, "emotion_labeling_task.html", task_to_throw)


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
    # which character?
        'character': "",
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
    # which character?
        'character': "",
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

    return render(request, "emotion_labeling_component_process_likert.html", task_to_throw)


def experiment2(request, video_title, wid, aid):
    Delete_Deprecated_Check_Task()

    exp_video = Experiment_Video.objects.filter(video_title = video_title)[0]
    if request.method=="POST":
        form = EmotionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])
        print(to_return)
        token = Experiment_Check_Store(exp_video, to_return, wid, aid)
        token = {'token': token}
        return render(request, "token_return.html", token)
    prompt_time = json.loads(exp_video.video_prompt_time)
    label_to_check = Experiment_Check_Task_Deployer(prompt_time, exp_video, wid, aid)
    """label_to_check = {
        6:{
            'valence': 2,
            'arousal': 2,
            'category': 'sadness',
            'reasoning': 'The face does look sad.',
        },
        26:{
            'valence': 3,
            'arousal': 8,
            'category': 'angry',
            'reasoning': 'She is confronting teacher.',
        },
    }"""
    task_to_throw = {
    # which video?
        'video_title': exp_video.video_title,
        'video_url': exp_video.video_url,
    # which character?
        'character': "",
    # in which condition?
        'condition': "experiment",
    # in which time do the system prompts?
        'prompt_time': exp_video.video_prompt_time,
        # additional info that is sent for sanity check
        'label_to_check': json.dumps(label_to_check),
        'step': "sanity_check",
    }
    return render(request, "emotion_labeling_task.html", task_to_throw)

def character_time_designator(request, title):
    video = Video_Before_Processing.objects.filter(video_title = title)[0]
    if request.method=="POST":
        form = EmotionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])

        save_character_time_data(to_return, title, video.video_url)


    task_to_throw ={
        'url': video.video_url,
    }
    return render(request, "character_time_designator.html", task_to_throw)

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
