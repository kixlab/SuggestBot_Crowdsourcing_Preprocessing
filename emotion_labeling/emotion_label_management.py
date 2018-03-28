from .models import *
import uuid
from django.db.models import Count, Min, F
from random import shuffle

EMO_VOTE_NUM = 3
TASK_TIME_LIMIT = 30
EMOTION_CATEGORY = [
  'fearful', 'angry', 'sad', 'disgusted', 'happy', 'surprised', 'frustrated', 'depressed', 'excited', 'neutral'
]
def Experiment_Label_Store(exp_video, result, w_id, a_id, condition):
    labels = result['labels']
    token = str(uuid.uuid4().hex.upper()[0:6])
    for time in labels:
        label = labels[time]
        print(label)
        label_ds = Emotion_label_experiment(experiment_video = exp_video, time=float(time), valence=int(label['valence']), arousal=int(label['arousal']), category = label['category'], reasoning = label['reasoning'], wid= w_id, aid= a_id, condition=condition)
        for emotion in label['minor_category']:
            if emotion in EMOTION_CATEGORY:
                if emotion == 'fearful':
                    label_ds.fearful_m = True
                elif emotion == 'angry':
                    label_ds.angry_m = True
                elif emotion == 'sad':
                    label_ds.sad_m = True
                elif emotion == 'disgusted':
                    label_ds.disgusted_m = True
                elif emotion == 'happy':
                    label_ds.happy_m = True
                elif emotion == 'surprised':
                    label_ds.surprised_m = True
                elif emotion == 'frustrated':
                    label_ds.frustrated_m = True
                elif emotion == 'depressed':
                    label_ds.depressed_m = True
                elif emotion == 'excited':
                    label_ds.excited_m = True
                elif emotion == 'neutral':
                    label_ds.neutral_m = True
            else:
                label_ds.other_m = emotion
        label_ds.save()

    return token

def Experiment_Check_Task_Deployer(prompt_time, video, w_id, a_id):
    return_dict = {}
    for key in prompt_time:
        # ** should only filter out those in 'experiment_reasoning' class! **
        filtered_labels = Emotion_label_experiment.objects.filter(experiment_video = video, time = key, condition='experiment_reasoning').annotate(num_task = Count('emotion_check_experiment')).filter(num_task__lt = EMO_VOTE_NUM)
        if filtered_labels.count() > 0:
            min_num_task = filtered_labels.aggregate(Min('num_task'))['num_task__min']
            print(min_num_task)
            filtered_labels = list(filtered_labels.filter(num_task = min_num_task))
            shuffle(filtered_labels)
            filtered_label = filtered_labels[0]
            emo_check = Emotion_check_experiment(emotion_label = filtered_label, wid=w_id, aid=a_id)
            emo_check.save()
            return_dict[filtered_label.time] = {
                'valence': filtered_label.valence,
                'arousal': filtered_label.arousal,
                'category': filtered_label.category,
                'reasoning': filtered_label.reasoning,
                'label_aid' : filtered_label.aid,
                'label_wid' : filtered_label.wid,
            }
        else:
            # TODO fill this exception handling
            print("Task already fully done.")
    print(return_dict)
    return return_dict

def Experiment_Check_Store(video, to_return, w_id, a_id):
    labels = to_return['labels']
    token = str(uuid.uuid4().hex.upper()[0:6])
    for time in labels:
        label_aid = labels[time]['label_aid']
        label_wid = labels[time]['label_wid']
        qualified = labels[time]['qualified']
        label = Emotion_label_experiment.objects.filter(wid=label_wid, aid=label_aid, time=time)[0]
        check = Emotion_check_experiment.objects.filter(wid= w_id, aid= a_id, emotion_label = label)
        if check.count() > 0:
            check = check[0]
            check.end_time = datetime.datetime.now()
            check.qualified = qualified
        else:
            check  = Emotion_check_experiment(wid=w_id, aid=a_id, emotion_label=label, start_time=datetime.datetime.now()-datetime.timedelta(minutes=10) , qualified=qualified)
        check.save()
    return token


def Delete_Deprecated_Check_Task():
    emo_check = Emotion_check_experiment.objects.filter(start_time__gte = F('end_time'), start_time__lte = datetime.datetime.now()-datetime.timedelta(minutes=TASK_TIME_LIMIT))
    emo_check.delete()
