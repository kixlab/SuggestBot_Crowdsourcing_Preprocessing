from .models import *
import uuid
def Experiment_Label_Store(exp_video, result, w_id, a_id):
    labels = result['labels']
    token = str(uuid.uuid4().hex.upper()[0:6])
    for time in labels:
        label = labels[time]
        label_ds = Emotion_label_experiment(experiment_video = exp_video, time=float(time), valence=int(label['valence']), arousal=int(label['arousal']), category = label['category'], reasoning = label['reasoning'], wid= w_id, aid= a_id)
        label_ds.save()

    return token
