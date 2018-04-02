from django.shortcuts import render, redirect, reverse
import json
from django.http import HttpResponse
from .forms import *
from .models import *
from .emotion_label_management import *
import uuid
# Create your views here.

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
