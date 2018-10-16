from django.db import models
import datetime
# Create your models here.

class Emotion_Video(models.Model):
    video_title = models.CharField(max_length = 200, default = "")
    video_url = models.CharField(max_length = 2000, default = "")
    video_img = models.CharField(max_length = 200, default = "")
    video_prompt_time = models.CharField(max_length=10000, default = "")
    def __str__(self):
        return self.video_title

class Emotion_Gold_Data(models.Model):
    emotion_video = models.ForeignKey('Emotion_Video', default=None, on_delete=models.CASCADE)
    end_time = models.DateTimeField(default = datetime.datetime.now)
    start_time = models.DateTimeField(default = datetime.datetime.now)
    gen_time = models.DateTimeField(default = datetime.datetime.now)
    emotion_confidences = models.CharField(max_length=20000, default = "")
    other = models.CharField(max_length=20000, default = "")
    wid = models.CharField(max_length=2000, default="")
    aid = models.CharField(max_length=2000, default="")
    task_time = models.IntegerField(default = "-1")
    token = models.CharField(max_length=200, default="")
    class Meta:
        abstract = True

class Emotion_Gold_Data_Checkbox(Emotion_Gold_Data):
    def model_name():
        return 'emotion_gold_data_checkbox'
    def __str__(self):
        return self.wid + str(self.emotion_video.video_title)

class Emotion_Gold_Data_Checkbox_Confidence(Emotion_Gold_Data):
    def model_name():
        return 'emotion_gold_data_checkbox_confidence'
    def __str__(self):
        return self.wid + str(self.emotion_video.video_title)

class Emotion_Gold_Data_Radio(Emotion_Gold_Data):
    def model_name():
        return 'emotion_gold_data_radio'
    def __str__(self):
        return self.wid + str(self.emotion_video.video_title)

class Emotion_Gold_Data_Distribution(Emotion_Gold_Data):
    def model_name():
        return 'emotion_gold_data_distribution'
    def __str__(self):
        return self.wid + str(self.emotion_video.video_title)

class Emotion_Task(models.Model):
    emotion_video = models.ForeignKey('Emotion_Video', default=None, on_delete=models.CASCADE)
    end_time = models.DateTimeField(default = datetime.datetime.now)
    start_time = models.DateTimeField(default = datetime.datetime.now)
    gen_time = models.DateTimeField(default = datetime.datetime.now)
    emotion_confidences = models.CharField(max_length=20000, default = "")
    other = models.CharField(max_length=20000, default = "")
    wid = models.CharField(max_length=2000, default="")
    aid = models.CharField(max_length=2000, default="")
    task_time = models.IntegerField(default = "-1")
    token = models.CharField(max_length=200, default="")
    survey_result = models.CharField(max_length = 20000, default="")
    class Meta:
        abstract = True

class Emotion_Task_Radio(Emotion_Task):
    def model_name():
        return 'emotion_task_radio'
    def __str__(self):
        return self.wid + str(self.emotion_video.video_title)

class Emotion_Task_Radio_Confidence(Emotion_Task):
    def model_name():
        return 'emotion_task_radio_confidence'
    def __str__(self):
        return self.wid + str(self.emotion_video.video_title)

class Emotion_Task_Checkbox(Emotion_Task):
    def model_name():
        return 'emotion_task_checkbox'
    def __str__(self):
        return self.wid + str(self.emotion_video.video_title)

class Emotion_Task_Checkbox_Confidence(Emotion_Task):
    def model_name():
        return 'emotion_task_checkbox_confidence'
    def __str__(self):
        return self.wid + str(self.emotion_video.video_title)


class Frame_Sentence(models.Model):
    sentence_id = models.IntegerField(default = -1)
    def __str__(self):
        return str(self.sentence_id)

class Frame_Sentence_GT(models.Model):
    sentence_id = models.IntegerField(default = -1)
    def __str__(self):
        return str(self.sentence_id)
class Frame_Task(models.Model):
    frame_sentence = models.ForeignKey('Frame_Sentence', default=None, on_delete=models.CASCADE)
    end_time = models.DateTimeField(default = datetime.datetime.now)
    start_time = models.DateTimeField(default = datetime.datetime.now)
    gen_time = models.DateTimeField(default = datetime.datetime.now)
    frame_confidences = models.CharField(max_length=20000, default = "")
    no_field_reasoning = models.CharField(max_length = 20000, default = "")
    wid = models.CharField(max_length=2000, default="")
    aid = models.CharField(max_length=2000, default="")
    task_sub_id = models.IntegerField(default = "-1")
    token = models.CharField(max_length=200, default="")
    survey_result = models.CharField(max_length = 20000, default="")
    class Meta:
        abstract = True

class Frame_Task_Radio(Frame_Task):
    def model_name():
        return 'frame_task_radio'
    def __str__(self):
        return self.wid + str(self.frame_sentence.sentence_id)

class Frame_Task_Radio_Confidence(Frame_Task):
    def model_name():
        return 'frame_task_radio_confidence'
    def __str__(self):
        return self.wid + str(self.frame_sentence.sentence_id)

class Frame_Task_Checkbox(Frame_Task):
    def model_name():
        return 'frame_task_checkbox'
    def __str__(self):
        return self.wid + str(self.frame_sentence.sentence_id)

class Frame_Task_Checkbox_Confidence(Frame_Task):
    def model_name():
        return 'frame_task_checkbox_confidence'
    def __str__(self):
        return self.wid + str(self.frame_sentence.sentence_id)


class Frame_Gold_Data(models.Model):
    frame_sentence = models.ForeignKey('Frame_Sentence_GT', default=None, on_delete=models.CASCADE)
    end_time = models.DateTimeField(default = datetime.datetime.now)
    start_time = models.DateTimeField(default = datetime.datetime.now)
    gen_time = models.DateTimeField(default = datetime.datetime.now)
    frame_confidences = models.CharField(max_length=20000, default = "")
    no_field_reasoning = models.CharField(max_length = 20000, default = "")
    wid = models.CharField(max_length=2000, default="")
    aid = models.CharField(max_length=2000, default="")
    task_sub_id = models.IntegerField(default = "-1")
    token = models.CharField(max_length=200, default="")
    class Meta:
        abstract = True

class Frame_Gold_Data_Checkbox(Frame_Gold_Data):
    def model_name():
        return 'frame_gold_data_checkbox'
    def __str__(self):
        return self.wid+ str(self.frame_sentence.sentence_id)

class Frame_Gold_Data_Checkbox_Confidence(Frame_Gold_Data):
    def model_name():
        return 'frame_gold_data_checkbox_confidence'
    def __str__(self):
        return self.wid+ str(self.frame_sentence.sentence_id)

class Frame_Gold_Data_Radio(Frame_Gold_Data):
    def model_name():
        return 'frame_gold_data_radio'
    def __str__(self):
        return self.wid+ str(self.frame_sentence.sentence_id)

class Frame(models.Model):
    frame_name = models.CharField(max_length=200, default="")
    frame_definition = models.CharField(max_length=20000, default="")
    def __str__(self):
        return self.frame_name

class Video_Before_Processing(models.Model):
    video_title = models.CharField(max_length = 200, default = "")
    video_url = models.CharField(max_length = 2000, default = "")
    def __str__(self):
        return self.video_title

#for multi interface study purpose
class Study_Video(models.Model):
    video_title = models.CharField(max_length = 200, default = "")
    video_url = models.CharField(max_length = 2000, default = "")
    video_img = models.CharField(max_length = 200, default = "")
    video_prompt_time = models.IntegerField(default = 0)
    def __str__(self):
        return self.video_title+"_"+str(self.video_prompt_time)

class Experiment_Video(models.Model):
    video_title = models.CharField(max_length = 200, default = "")
    video_url = models.CharField(max_length = 2000, default = "")
    video_img = models.CharField(max_length = 200, default = "")
    video_prompt_time = models.CharField(max_length=10000, default = "")
    video_total_time = models.IntegerField(default = 0)
    video_prompt_num = models.IntegerField(default = 0)
    video_hit_dict = models.CharField(max_length = 200000, default = "", null=True, blank=True)
    def __str__(self):
        return self.video_title

class Emotion_label_Meta(models.Model):
    #video_url = models.CharField(max_length=200, default = "")
    #character = models.CharField(max_length=200, default = "")
    time = models.IntegerField(default = 0)
    valence = models.IntegerField(default = 0)
    arousal = models.IntegerField(default = 0)
    category = models.CharField(max_length = 50, default = "")
    fearful_m =models.BooleanField(default = False)
    angry_m =models.BooleanField(default = False)
    sad_m =models.BooleanField(default = False)
    disgusted_m =models.BooleanField(default = False)
    happy_m =models.BooleanField(default = False)
    surprised_m =models.BooleanField(default = False)
    frustrated_m =models.BooleanField(default = False)
    depressed_m =models.BooleanField(default = False)
    excited_m =models.BooleanField(default = False)
    neutral_m =models.BooleanField(default = False)
    other_m =models.CharField(default = 'other', max_length=100)
    reasoning = models.TextField(max_length = 10000, default = "")
    wid = models.CharField(max_length = 200, default="")
    aid = models.CharField(max_length = 200, default="")
    task_end_time = models.DateTimeField(default = datetime.datetime.now)

class Emotion_check_Meta(models.Model):
    qualified = models.BooleanField(default = False)
    end_time = models.DateTimeField(default = datetime.datetime.now)
    start_time = models.DateTimeField(default = datetime.datetime.now)
    wid = models.CharField(max_length = 200, default = "")
    aid = models.CharField(max_length = 200, default = "")
    class Meta:
        abstract = True


class Emotion_label_experiment(Emotion_label_Meta):
    experiment_video = models.ForeignKey(Experiment_Video, on_delete=models.CASCADE, null=True, blank=True)
    condition = models.CharField(max_length = 200, default = "")
    def __str__(self):
        return self.experiment_video.video_title + "_" + str(self.time) +"_from_worker_" +self.wid

class Emotion_Label_Component_Process(Emotion_label_Meta):
    experiment_video = models.ForeignKey(Experiment_Video, on_delete=models.CASCADE, null=True, blank=True)
    smiling = models.BooleanField(default = False)
    mouth_opening = models.BooleanField(default = False)
    mouth_closing = models.BooleanField(default = False)
    mouth_tensing= models.BooleanField(default = False)
    frown = models.BooleanField(default = False)
    tears = models.BooleanField(default = False)
    eyes_opening = models.BooleanField(default = False)
    eyes_closing = models.BooleanField(default = False)
    volume_increasing = models.BooleanField(default = False)
    volume_decreasing = models.BooleanField(default = False)
    v_trembling = models.BooleanField(default = False)
    v_assertive = models.BooleanField(default = False)
    g_abrupt = models.BooleanField(default = False)
    moving_towards = models.BooleanField(default = False)
    withdrawing = models.BooleanField(default = False)
    against = models.BooleanField(default = False)
    silence = models.BooleanField(default = False)
    short_utterance = models.BooleanField(default = False)
    long_utterance = models.BooleanField(default = False)
    s_melody = models.BooleanField(default = False)
    s_disturbance = models.BooleanField(default = False)
    s_tempo = models.BooleanField(default = False)
    shiver = models.BooleanField(default = False)
    pale = models.BooleanField(default = False)
    breathing_slow = models.BooleanField(default = False)
    breathing_faster = models.BooleanField(default = False)
    sweating = models.BooleanField(default = False)
    blushing = models.BooleanField(default = False)
    cog_motiv = models.CharField(max_length=10000, default="")
    #motivational = models.CharField(max_length=10000, default="")

#for pre data collection
class Emotion_Label_Component_Process_Likert(Emotion_label_Meta):
    experiment_video = models.ForeignKey(Experiment_Video, on_delete=models.CASCADE, null=True, blank=True)
    smiling = models.IntegerField(default = 1)
    mouth_close_open = models.IntegerField(default = 3)
    mouth_tensing= models.IntegerField(default = 1)
    frowning = models.IntegerField(default = 1)
    tear = models.IntegerField(default = 1)
    eyes_close_open = models.IntegerField(default = 3)
    volume_volume = models.IntegerField(default = 3)
    voice_trembling = models.IntegerField(default = 1)
    voice_assertive = models.IntegerField(default = 3)
    body_abrupt = models.IntegerField(default = 1)
    towards = models.IntegerField(default = 1)
    withdrawing = models.IntegerField(default = 1)
    against = models.IntegerField(default = 1)
    utterance_length = models.IntegerField(default = 3)
    speech_melody = models.IntegerField(default = 1)
    speech_disturbed = models.IntegerField(default = 1)
    speech_tempo = models.IntegerField(default = 3)
    shiver = models.IntegerField(default = 1)
    pale = models.IntegerField(default = 1)
    breathing = models.IntegerField(default = 3)
    sweating = models.IntegerField(default = 1)
    blushing = models.IntegerField(default = 1)

    sudden = models.IntegerField(default = 1)
    probable = models.IntegerField(default = 1)
    pleasant = models.IntegerField(default = 1)
    chance = models.IntegerField(default = 1)
    own = models.IntegerField(default = 1)
    other = models.IntegerField(default = 1)
    intentionally = models.IntegerField(default = 1)
    norm = models.IntegerField(default = 1)
    goal = models.IntegerField(default = 1)
    expected = models.IntegerField(default = 1)
    consistency = models.IntegerField(default = 1)
    envisaged = models.IntegerField(default = 1)
    consequence = models.IntegerField(default = 1)
    immediate = models.IntegerField(default = 1)
    avoidable = models.IntegerField(default = 1)
    adjustable = models.IntegerField(default = 1)
    attention_event = models.IntegerField(default = 1)
    searching_info = models.IntegerField(default = 1)
    attention_people = models.IntegerField(default = 1)
    physical_event = models.IntegerField(default = 1)
    not_sure_reasoning = models.CharField(default="", max_length=1000)

#data structure for baseline condition
class Emotion_Label_Baseline(Emotion_label_Meta):
    experiment_video = models.ForeignKey(Experiment_Video, on_delete=models.CASCADE, null=True, blank=True)

#for component process (later used for priming conditions and model infer condition)
class Emotion_Label_Component_Process_Only(models.Model):
    time = models.IntegerField(default = 0)
    wid = models.CharField(max_length = 200, default="")
    aid = models.CharField(max_length = 200, default="")
    task_end_time = models.DateTimeField(default = datetime.datetime.now)
    experiment_video = models.ForeignKey(Experiment_Video, on_delete=models.CASCADE, null=True, blank=True)
    smiling = models.IntegerField(default = 1)
    mouth_close_open = models.IntegerField(default = 3)
    mouth_tensing= models.IntegerField(default = 1)
    frowning = models.IntegerField(default = 1)
    tear = models.IntegerField(default = 1)
    eyes_close_open = models.IntegerField(default = 3)
    volume_volume = models.IntegerField(default = 3)
    voice_trembling = models.IntegerField(default = 1)
    voice_assertive = models.IntegerField(default = 3)
    body_abrupt = models.IntegerField(default = 1)
    towards = models.IntegerField(default = 1)
    withdrawing = models.IntegerField(default = 1)
    against = models.IntegerField(default = 1)
    utterance_length = models.IntegerField(default = 3)
    speech_melody = models.IntegerField(default = 1)
    speech_disturbed = models.IntegerField(default = 1)
    speech_tempo = models.IntegerField(default = 3)
    shiver = models.IntegerField(default = 1)
    pale = models.IntegerField(default = 1)
    breathing = models.IntegerField(default = 3)
    sweating = models.IntegerField(default = 1)
    blushing = models.IntegerField(default = 1)

    sudden = models.IntegerField(default = 1)
    probable = models.IntegerField(default = 1)
    pleasant = models.IntegerField(default = 1)
    chance = models.IntegerField(default = 1)
    own = models.IntegerField(default = 1)
    other = models.IntegerField(default = 1)
    intentionally = models.IntegerField(default = 1)
    norm = models.IntegerField(default = 1)
    goal = models.IntegerField(default = 1)
    expected = models.IntegerField(default = 1)
    consistency = models.IntegerField(default = 1)
    envisaged = models.IntegerField(default = 1)
    consequence = models.IntegerField(default = 1)
    immediate = models.IntegerField(default = 1)
    avoidable = models.IntegerField(default = 1)
    adjustable = models.IntegerField(default = 1)
    attention_event = models.IntegerField(default = 1)
    searching_info = models.IntegerField(default = 1)
    attention_people = models.IntegerField(default = 1)
    physical_event = models.IntegerField(default = 1)
    not_sure_reasoning = models.CharField(default="", max_length=1000)

class Emotion_Distribution_Meta(models.Model):
    #video_url = models.CharField(max_length=200, default = "")
    #character = models.CharField(max_length=200, default = "")
    experiment_video = models.ForeignKey(Experiment_Video, on_delete=models.CASCADE, null=True, blank=True)
    time = models.IntegerField(default = 0)
    distribution = models.CharField(max_length = 20000, default="")
    wid = models.CharField(max_length = 200, default="")
    aid = models.CharField(max_length = 200, default="")
    task_start_time = models.DateTimeField(default = datetime.datetime.now)
    task_end_time = models.DateTimeField(default = datetime.datetime.now)
    class Meta:
        abstract = True

class Emotion_Distribution_Collection(Emotion_Distribution_Meta):
    def __str__(self):
        return self.experiment_video.video_title + "_" + str(self.time) + "_" + self.wid

#example object - store data as raw counts
class Emotion_Distribution_Example(models.Model):
    experiment_video = models.ForeignKey(Experiment_Video, on_delete=models.CASCADE, null=True, blank=True)
    time = models.IntegerField(default = 0)
    distribution = models.CharField(max_length = 20000, default = "")
    def __str__(self):
        return self.experiment_video.video_title + "_" + str(self.time)

class Emotion_check_experiment(Emotion_check_Meta):
    emotion_label = models.ForeignKey(Emotion_label_experiment, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.emotion_label.experiment_video.video_title + "_" + str(self.emotion_label.time)+ "_by_" + self.emotion_label.wid+"check_result"

class Bonus_Paid(models.Model):
    wid = models.CharField(default="", max_length=2000)
    aid = models.CharField(default="", max_length=2000)
    hid = models.CharField(default="", max_length=2000)
    def __str__(self):
        return self.wid+"_"+self.aid
