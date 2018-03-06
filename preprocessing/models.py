from django.db import models

# Create your models here.

#class for the video. Each contains url and decision on whether it passed or not.
class Video(models.Model):
    video_title = models.CharField(max_length = 200, default = "")
    video_url = models.CharField(max_length = 200, default = "")
    # whether 3 inspeciton votes are collected for this video
    fully_inspected = models.BooleanField(default = False)
    # whether this video can be further utilized for emotion and intention labeling or not
    passed = models.BooleanField(default = False)
    def __str__(self):
        return self.video_title

class Video_inspection_vote(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    video_quality = models.BooleanField(default = False)
    sound_quality = models.BooleanField(default = False)
    language = models.BooleanField(default = False)
    conversation = models.BooleanField(default = False)
    scene = models.BooleanField(default = False)
