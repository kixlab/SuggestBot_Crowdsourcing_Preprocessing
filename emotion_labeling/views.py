from django.shortcuts import render
import json
from .forms import *
from .models import *
from .emotion_label_management import *
# Create your views here.
def experiment1(request, video_title, wid, aid):
    exp_video = Experiment_Video.objects.filter(video_title = video_title)[0]
    if request.method=="POST":
        form = EmotionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])
        token = Experiment_Label_Store(exp_video, to_return, wid, aid)
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
    # in which condition?
        'condition': "experiment",
    # in which time do the system prompts?
        'prompt_time': exp_video.video_prompt_time,
    # additional info that is sent for sanity check
        'label_to_check': json.dumps({}),
        'step': "label_and_reason",
    }
    # *** for images, you should store them in '/static/img/figures/{{condition}}/{{video_url}}/{{video_url}}{{character}}'
    # based on the condition, url will be differently assigned

    return render(request, "emotion_labeling_task.html", task_to_throw)


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
