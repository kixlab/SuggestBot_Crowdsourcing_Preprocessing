from django.db import models
import datetime
# Create your models here.
class Experiment_Video(models.Model):
    video_title = models.CharField(max_length = 200, default = "")
    video_url = models.CharField(max_length = 200, default = "")
    video_prompt_time = models.CharField(max_length=10000, default = "")
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

class Emotion_check_experiment(Emotion_check_Meta):
    emotion_label = models.ForeignKey(Emotion_label_experiment, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.emotion_label.experiment_video.video_title + "_" + str(self.emotion_label.time)+ "_by_" + self.emotion_label.wid+"check_result"
