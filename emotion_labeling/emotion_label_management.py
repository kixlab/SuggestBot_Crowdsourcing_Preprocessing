from .models import *
import uuid
from django.db.models import Count, Min, F
from random import shuffle
import json

EMO_VOTE_NUM = 3
TASK_TIME_LIMIT = 30
EMOTION_CATEGORY = [
  'fearful', 'angry', 'sad', 'disgusted', 'happy', 'surprised', 'frustrated', 'depressed', 'excited', 'neutral'
]
def Experiment_Label_Baseline_Store(exp_video, result, w_id, a_id):
    labels = result['labels']
    token = str(uuid.uuid4().hex.upper()[0:6])
    for time in labels:
        label = labels[time]
        print(label)
        label_ds = Emotion_Label_Baseline(experiment_video = exp_video, time=float(time), valence=int(label['valence']), arousal=int(label['arousal']), category = label['category'], reasoning = label['reasoning'], wid= w_id, aid= a_id)
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

def Experiment_Label_Component_Process_Store(exp_video, result, w_id, a_id):
    labels = result['labels']
    token = str(uuid.uuid4().hex.upper()[0:6])
    for time in labels:
        label = labels[time]
        print(label)
        label_ds = Emotion_Label_Component_Process(experiment_video = exp_video, time=float(time), valence=int(label['valence']), arousal=int(label['arousal']), category = label['category'], reasoning = label['reasoning'], wid= w_id, aid= a_id)
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
        for motor in label['motor']:
            if motor == 'smiling':
                label_ds.smiling = True
            elif motor == 'mouth_opening':
                label_ds.mouth_opening = True
            elif motor == 'mouth_closing':
                label_ds.mouth_closing = True
            elif motor == 'mouth_tensing':
                label_ds.mouth_tensing = True
            elif motor == 'eyes_closing':
                label_ds.eyes_closing = True
            elif motor == 'frown':
                label_ds.frown = True
            elif motor == 'tears':
                label_ds.tears = True
            elif motor == 'eyes_opening':
                label_ds.eyes_opening = True
            elif motor == 'volume_increasing':
                label_ds.volume_increasing = True
            elif motor == 'volume_decreasing':
                label_ds.volume_decreasing = True
            elif motor == 'v_trembling':
                label_ds.v_trembling = True
            elif motor == 'v_assertive':
                label_ds.v_assertive = True
            elif motor == 'g_abrupt':
                label_ds.g_abrupt = True
            elif motor == 'moving_towards':
                label_ds.moving_towards = True
            elif motor == 'withdrawing':
                label_ds.withdrawing = True
            elif motor == 'against':
                label_ds.against = True
            elif motor == 'silence':
                label_ds.silence = True
            elif motor == 'short_utterance':
                label_ds.short_utterance = True
            elif motor == 'long_utterance':
                label_ds.long_utterance = True
            elif motor == 's_melody':
                label_ds.s_melody = True
            elif motor == 's_disturbance':
                label_ds.s_disturbance = True
            elif motor == 's_tempo':
                label_ds.s_tempo = True

        for physio in label['physio']:
            if physio == 'shiver':
                label_ds.shiver = True
            elif physio == 'pale':
                label_ds.pale = True
            elif physio == 'breathing_slow':
                label_ds.pale = True
            elif physio == 'breathing_faster':
                label_ds.pale = True
            elif physio == 'sweating':
                label_ds.pale = True
            elif physio == 'blushing':
                label_ds.pale = True

        label_ds.cog_motiv = label['cog_motiv']
        #label_ds.motivational = label['motivational']
        print(label_ds)
        label_ds.save()

    return token

def Experiment_Label_Component_Process_Store_Likert(exp_video, result, w_id, a_id):
    labels = result['labels']
    token = str(uuid.uuid4().hex.upper()[0:6])
    for time in labels:
        label = labels[time]
        print(label)
        label_ds = Emotion_Label_Component_Process_Likert(experiment_video = exp_video, time=float(time), valence=int(label['valence']), arousal=int(label['arousal']), category = label['category'], wid= w_id, aid= a_id)
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
        reason_dict = {}
        for cp in label['component_process']:
            if len(label['component_process'][cp])> 4:
                reason_dict[cp] = label['component_process'][cp]
            else:
                if cp == 'smiling':
                    label_ds.smiling = int(label['component_process'][cp])
                elif cp == 'mouth_close_open':
                    label_ds.mouth_close_open = int(label['component_process'][cp])
                elif cp == 'mouth_tensing':
                    label_ds.mouth_tensing = int(label['component_process'][cp])
                elif cp == 'frowning':
                    label_ds.frowning = int(label['component_process'][cp])
                elif cp == 'tear':
                    label_ds.tear = int(label['component_process'][cp])
                elif cp == 'eyes_close_open':
                    label_ds.eyes_close_open = int(label['component_process'][cp])
                elif cp == 'voice_volume':
                    label_ds.voice_volume = int(label['component_process'][cp])
                elif cp == 'voice_trembling':
                    label_ds.voice_trembling = int(label['component_process'][cp])
                elif cp == 'voice_assertive':
                    label_ds.voice_assertive = int(label['component_process'][cp])
                elif cp == 'body_abrupt':
                    label_ds.body_abrupt = int(label['component_process'][cp])
                elif cp == 'towards':
                    label_ds.towards = int(label['component_process'][cp])
                elif cp == 'withdrawing':
                    label_ds.withdrawing = int(label['component_process'][cp])
                elif cp == 'against':
                    label_ds.against = int(label['component_process'][cp])
                elif cp == 'utterance_length':
                    label_ds.utterance_length = int(label['component_process'][cp])
                elif cp == 'speech_melody':
                    label_ds.speech_melody = int(label['component_process'][cp])
                elif cp == 'speech_disturbed':
                    label_ds.speech_disturbed = int(label['component_process'][cp])
                elif cp == 'speech_tempo':
                    label_ds.speech_tempo = int(label['component_process'][cp])
                elif cp == 'shiver':
                    label_ds.shiver = int(label['component_process'][cp])
                elif cp == 'pale':
                    label_ds.pale = int(label['component_process'][cp])
                elif cp == 'breathing':
                    label_ds.breathing = int(label['component_process'][cp])
                elif cp == 'sweating':
                    label_ds.sweating = int(label['component_process'][cp])
                elif cp == 'blushing':
                    label_ds.blushing = int(label['component_process'][cp])
                elif cp == 'sudden':
                    label_ds.sudden = int(label['component_process'][cp])
                elif cp == 'probable':
                    label_ds.probable = int(label['component_process'][cp])
                elif cp == 'pleasant':
                    label_ds.pleasant = int(label['component_process'][cp])
                elif cp == 'chance':
                    label_ds.chance = int(label['component_process'][cp])
                elif cp == 'own':
                    label_ds.own = int(label['component_process'][cp])
                elif cp == 'other':
                    label_ds.other = int(label['component_process'][cp])
                elif cp == 'intentionally':
                    label_ds.intentionally = int(label['component_process'][cp])
                elif cp == 'norm':
                    label_ds.norm = int(label['component_process'][cp])
                elif cp == 'goal':
                    label_ds.goal = int(label['component_process'][cp])
                elif cp == 'expected':
                    label_ds.expected = int(label['component_process'][cp])
                elif cp == 'consistency':
                    label_ds.consistency = int(label['component_process'][cp])
                elif cp == 'envisaged':
                    label_ds.envisaged = int(label['component_process'][cp])
                elif cp == 'consequence':
                    label_ds.consequence = int(label['component_process'][cp])
                elif cp == 'immediate':
                    label_ds.immediate = int(label['component_process'][cp])
                elif cp == 'avoidable':
                    label_ds.avoidable = int(label['component_process'][cp])
                elif cp == 'adjustable':
                    label_ds.adjustable = int(label['component_process'][cp])
                elif cp == 'attention_event':
                    label_ds.attention_event = int(label['component_process'][cp])
                elif cp == 'searching_info':
                    label_ds.searching_info = int(label['component_process'][cp])
                elif cp == 'attention_people':
                    label_ds.attention_people = int(label['component_process'][cp])
                elif cp == 'physical_event':
                    label_ds.physical_event = int(label['component_process'][cp])
        print(label_ds)
        print(reason_dict)
        label_ds.not_sure_reasoning = json.dumps(reason_dict)
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
