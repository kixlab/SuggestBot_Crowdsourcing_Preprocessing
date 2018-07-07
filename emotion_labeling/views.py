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
from dateutil import tz
# Create your views here.
TIME_ZONE_LOCAL = tz.tzlocal()
TIME_ZONE_UTC = tz.gettz('UTC')

def study_emotion_prev(request, wid, aid):
   # initialize_frame_sentences()
    #TODO delete deprecated task items - all the tasks by none-paid workers should be deleted!
    for emotion_task_model in [Emotion_Task_Radio, Emotion_Task_Radio_Confidence, Emotion_Task_Checkbox, Emotion_Task_Checkbox_Confidence,]:
        et_to_deletes = emotion_task_model.objects.filter(gen_time__gte = F('end_time'), gen_time__lte = datetime.datetime.now()-datetime.timedelta(minutes=TASK_TIME_LIMIT))
        for et_to_delete in et_to_deletes:
            emotion_task_model.objects.filter(wid = ft_to_delete.wid, aid = ft_to_delete.aid).delete()
    min_key = None
    for emotion_task_model in [Emotion_Task_Radio,  Emotion_Task_Radio_Confidence, Emotion_Task_Checkbox, Emotion_Task_Checkbox_Confidence,]:
        if emotion_task_model.objects.filter(wid=wid).count() > 0:
            if emotion_task_model == Emotion_Task_Radio:
                min_key = 'Radio'
            elif emotion_task_model == Emotion_Task_Radio_Confidence:
                min_key = 'Radio_Confidence'
            elif emotion_task_model == Emotion_Task_Checkbox:
                min_key = 'Checkbox'
            elif emotion_task_model == Emotion_Task_Checkbox_Confidence:
                min_key = 'Checkbox_Confidence'
    if min_key == None:
        count_dic = {}
        count_dic['Radio'] = Emotion_Task_Radio.objects.all().count()
        count_dic['Radio_Confidence'] = Emotion_Task_Radio_Confidence.objects.all().count()
        count_dic['Checkbox'] = Emotion_Task_Checkbox.objects.all().count()
        count_dic['Checkbox_Confidence']=Emotion_Task_Checkbox_Confidence.objects.all().count()
        min_key = min(count_dic, key=count_dic.get)
    return redirect('/emotion_labeling/study_emotion/'+min_key+'/'+wid+'/'+aid)

def study_emotion(request, condition, wid, aid):
    print(wid)
    if condition == "Radio":
        emotion_task_model = Emotion_Task_Radio
    elif condition == "Radio_Confidence":
        emotion_task_model = Emotion_Task_Radio_Confidence
    elif condition == "Checkbox":
        emotion_task_model = Emotion_Task_Checkbox
    elif condition == "Checkbox_Confidence":
        emotion_task_model = Emotion_Task_Checkbox_Confidence

    #initialize_frame_sentences()
    if request.method=="POST":
        #TODO save items
        #TODO update Frame Task
        form = EmotionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])
        if emotion_task_model.objects.filter(wid=wid, aid=aid).count()==0:
            return HttpResponse("You were late in completing the task, so your task is expired.")
        token_string = str(uuid.uuid4().hex.upper()[0:6])
        for key in to_return:
            task_obj = emotion_task_model.objects.filter(wid=wid, aid=aid, task_time=int(key))[0]
            task_obj.emotion_confidences = json.dumps(to_return[key]['emotion_confidence'])
            task_obj.survey_result = json.dumps(to_return[key]['survey_result'])
            s_time = datetime.datetime.strptime(to_return[key]['start_time'], "%a, %d %b %Y %H:%M:%S %Z")
            s_time = s_time.replace(tzinfo = TIME_ZONE_UTC)
            task_obj.start_time = s_time.astimezone(TIME_ZONE_LOCAL)
            e_time = datetime.datetime.strptime(to_return[key]['end_time'], "%a, %d %b %Y %H:%M:%S %Z")
            e_time = e_time.replace(tzinfo = TIME_ZONE_UTC)
            task_obj.end_time = e_time.astimezone(TIME_ZONE_LOCAL)
            task_obj.token = token_string
            if 'other' in to_return[key]:
                task_obj.other = to_return[key]['other']
            task_obj.save()


        token = {'token':token_string}
        return render(request, "token_return.html", token)

    if emotion_task_model.objects.filter(wid=wid, aid=aid).count() == 0:
        #TODO generate 6 Emotion_Task items including sanity check
        taskable_video = Emotion_Video.objects.annotate(num_task=Count(emotion_task_model.model_name())).filter(num_task__lt=TARGET_TASK_NUM)
        min_ = taskable_video.aggregate(min_num_task=Min('num_task'))
        min_num_task = min_['min_num_task']
        taskable_video = taskable_video.filter(num_task = min_num_task)
        if taskable_video.count()==0:
            return HttpResponse("Sorry, you have done all the task you can do, or there is no more of available task.")
        else:
            e_video = taskable_video[random.randint(0, taskable_video.count()-1)]
            video_prompt_times = json.loads(e_video.video_prompt_time)
            for video_prompt_time in video_prompt_times:
                video_task = emotion_task_model(emotion_video = e_video, wid = wid, aid = aid, task_time=int(video_prompt_time))
                video_task.save()
    else:
        e_video = emotion_task_model.objects.filter(wid=wid, aid=aid)[0].emotion_video

    #frame = get_frame_from_database()
    print(e_video)
    to_send = {
        'prompt_time': e_video.video_prompt_time,
        'video_img': e_video.video_img,
        'video_url': e_video.video_url,
    }
    return render(request, "study_emotion_"+condition.lower()+".html", to_send)


def open_sentence(request, num):
    frame = get_frame_from_database(int(num))
    #frame = get_frame_from_database()
    to_send = {
        'task_num' :0,
        'frame' : frame,
    }
    return render(request, "study_frame_radio.html", to_send)

def gold_data_gather_frame(request, condition, wid, aid, task_num):
    for frame_task_model in [Frame_Gold_Data_Checkbox,  Frame_Gold_Data_Checkbox_Confidence,]:
        ft_to_deletes = frame_task_model.objects.filter(gen_time__gte = F('end_time'), gen_time__lte = datetime.datetime.now()-datetime.timedelta(minutes=2))
        for ft_to_delete in ft_to_deletes:
            frame_task_model.objects.filter(wid = ft_to_delete.wid, aid = ft_to_delete.aid).delete()
    print(wid)
    if condition == "Checkbox":
        frame_task_model = Frame_Gold_Data_Checkbox
    elif condition == "Checkbox_Confidence":
        frame_task_model = Frame_Gold_Data_Checkbox_Confidence

    #initialize_frame_sentences()
    if request.method=="POST":
        #TODOdone...? save items
        #TODOdone...? update Frame Task
        form = FrameStudyResult(request.POST)
        frame_task = frame_task_model.objects.get(task_sub_id = int(task_num) ,wid=wid, aid=aid)
        frame_task.end_time = datetime.datetime.now()
        print(form)
        frame_task.frame_confidences = form.cleaned_data['frame_confidences']
        frame_task.no_field_reasoning = form.cleaned_data['no_field_reasoning']
        frame_task.save()
        if int(task_num) != 5:
            return redirect("/emotion_labeling/gold_data_gather_frame/"+condition+'/'+wid+'/'+aid+'/'+str(int(task_num)+1))
        else:
            token_string = str(uuid.uuid4().hex.upper()[0:6])
            frame_task_model.objects.filter(wid=wid, aid=aid).update(token = token_string)
            token = {'token':token_string}
            return render(request, "token_return.html", token)

    if int(task_num) == 0 and frame_task_model.objects.filter(wid=wid, aid=aid).count() == 0:
        #TODOdone...? generate 6 Frame_Task items including sanity check
        taskable = frame_initialize_worker(wid, aid, frame_task_model, Frame_Sentence_GT, 50)
        frame = get_frame_from_database(INITIAL_TASK_SENTENCE)
        if not taskable:
            return HttpResponse("Sorry, you have done all the task you can do, or there is no more of available task.")
    else:
        #TODOdone..? get the frame sentence number from previously generated taks
        target_task = frame_task_model.objects.filter(wid=wid, aid=aid, task_sub_id=int(task_num))[0]
        target_task.start_time = datetime.datetime.now()
        target_task.save()
        target_sentence = target_task.frame_sentence.sentence_id
        frame = get_frame_from_database(target_sentence)
    #frame = get_frame_from_database()
    to_send = {
        'task_num' :task_num,
        'frame' : frame,
    }
    return render(request, "frame_gt_"+condition.lower()+".html", to_send)


def study_frame_prev(request, wid, aid):
   # initialize_frame_sentences()
    #TODOdone...? delete deprecated task items - all the tasks by none-paid workers should be deleted!
    for frame_task_model in [Frame_Task_Radio,  Frame_Task_Radio_Confidence, Frame_Task_Checkbox, Frame_Task_Checkbox_Confidence,]:
        ft_to_deletes = frame_task_model.objects.filter(gen_time__gte = F('end_time'), gen_time__lte = datetime.datetime.now()-datetime.timedelta(minutes=TASK_TIME_LIMIT))
        for ft_to_delete in ft_to_deletes:
            frame_task_model.objects.filter(wid = ft_to_delete.wid, aid = ft_to_delete.aid).delete()
    min_key = None
    for frame_task_model in [Frame_Task_Radio,  Frame_Task_Radio_Confidence, Frame_Task_Checkbox, Frame_Task_Checkbox_Confidence,]:
        if frame_task_model.objects.filter(wid=wid).count() > 0:
            if frame_task_model == Frame_Task_Radio:
                min_key = 'Radio'
            elif frame_task_model == Frame_Task_Radio_Confidence:
                min_key = 'Radio_Confidence'
            elif frame_task_model == Frame_Task_Checkbox:
                min_key = 'Checkbox'
            elif frame_task_model == Frame_Task_Checkbox_Confidence:
                min_key = 'Checkbox_Confidence'
    if min_key == None:
        count_dic = {}
        count_dic['Radio'] = Frame_Task_Radio.objects.all().count()
        count_dic['Radio_Confidence'] = Frame_Task_Radio_Confidence.objects.all().count()
        count_dic['Checkbox'] = Frame_Task_Checkbox.objects.all().count()
        count_dic['Checkbox_Confidence']=Frame_Task_Checkbox_Confidence.objects.all().count()
        min_key = min(count_dic, key=count_dic.get)
    return redirect('/emotion_labeling/study_frame/'+min_key+'/'+wid+'/'+aid+'/0')


def study_frame(request, condition, wid, aid, task_num):
    print(wid)
    if condition == "Radio":
        frame_task_model = Frame_Task_Radio
    elif condition == "Radio_Confidence":
        frame_task_model = Frame_Task_Radio_Confidence
    elif condition == "Checkbox":
        frame_task_model = Frame_Task_Checkbox
    elif condition == "Checkbox_Confidence":
        frame_task_model = Frame_Task_Checkbox_Confidence

    #initialize_frame_sentences()
    if request.method=="POST":
        #TODOdone...? save items
        #TODOdone...? update Frame Task
        form = FrameStudyResult(request.POST)
        frame_task = frame_task_model.objects.get(task_sub_id = int(task_num) ,wid=wid, aid=aid)
        frame_task.end_time = datetime.datetime.now()
        print(form)
        frame_task.frame_confidences = form.cleaned_data['frame_confidences']
        frame_task.no_field_reasoning = form.cleaned_data['no_field_reasoning']
        frame_task.save()
        return redirect("/emotion_labeling/nasa_tlx/"+condition+'/'+wid+'/'+aid+'/'+str(int(task_num)))

    if int(task_num) == 0 and frame_task_model.objects.filter(wid=wid, aid=aid).count() == 0:
        #TODOdone...? generate 6 Frame_Task items including sanity check
        taskable = frame_initialize_worker(wid, aid, frame_task_model, Frame_Sentence, TARGET_TASK_NUM)
        frame = get_frame_from_database(INITIAL_TASK_SENTENCE)
        if not taskable:
            return HttpResponse("Sorry, you have done all the task you can do, or there is no more of available task.")
    else:
        #TODOdone..? get the frame sentence number from previously generated taks
        target_task = frame_task_model.objects.filter(wid=wid, aid=aid, task_sub_id=int(task_num))[0]
        target_task.start_time = datetime.datetime.now()
        target_task.save()
        target_sentence = target_task.frame_sentence.sentence_id
        frame = get_frame_from_database(target_sentence)
    #frame = get_frame_from_database()
    to_send = {
        'task_num' :task_num,
        'frame' : frame,
    }
    return render(request, "study_frame_"+condition.lower()+".html", to_send)

def nasa_tlx(request, condition, wid, aid, task_num):
    if request.method=="POST":
        if condition == "Radio":
            frame_task_model = Frame_Task_Radio
        elif condition == "Radio_Confidence":
            frame_task_model = Frame_Task_Radio_Confidence
        elif condition == "Checkbox":
            frame_task_model = Frame_Task_Checkbox
        elif condition == "Checkbox_Confidence":
            frame_task_model = Frame_Task_Checkbox_Confidence
        #TODO save nasa tlx result
        form = SurveyResult(request.POST)
        print(form)
        frame_task = frame_task_model.objects.filter(wid=wid, aid=aid, task_sub_id = task_num)[0]
        frame_task.survey_result = form.cleaned_data['survey_result']
        frame_task.save()

        if int(task_num)!=TOTAL_SUB_TASK_NUM-1:
            return redirect('/emotion_labeling/study_frame/'+condition+'/'+wid+'/'+aid+'/'+str(int(task_num)+1))
        else:
            #TODOdone...? save token infos
            token_string = str(uuid.uuid4().hex.upper()[0:6])

            frame_task_model.objects.filter(wid=wid, aid=aid).update(token = token_string)
            token = {'token':token_string}
            return render(request, "token_return.html", token)
    return render(request, "nasa_tlx.html", {'task_num': task_num})



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
    pick_and_save_frame()
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
