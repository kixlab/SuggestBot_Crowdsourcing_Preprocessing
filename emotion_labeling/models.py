from django.db import models

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
    time = models.FloatField(default = 0)
    valence = models.IntegerField(default = 0)
    arousal = models.IntegerField(default = 0)
    category = models.CharField(max_length = 50, default = "")
    reasoning = models.TextField(max_length = 10000, default = "")
    wid = models.CharField(max_length = 200, default="")
    aid = models.CharField(max_length = 200, default="")

class Emotion_label_experiment(Emotion_label_Meta):
    experiment_video = models.ForeignKey(Experiment_Video, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.experiment_video.video_title + "_" + str(self.time)
