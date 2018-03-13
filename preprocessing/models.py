from django.db import models
import datetime
# Create your models here.

#class for the video. Each contains url and decision on whether it passed or not.
class Video(models.Model):
    video_title = models.CharField(max_length = 200, default = "")
    video_url = models.CharField(max_length = 200, default = "")
    # whether 3 inspeciton votes are collected for this video
    fully_inspected = models.BooleanField(default = False)
    # whether this video can be further utilized for emotion and intention labeling or not
    video_quality_passed = models.BooleanField(default = False)
    sound_quality_passed = models.BooleanField(default = False)
    language_passed = models.BooleanField(default = False)
    conversation_passed = models.BooleanField(default = False)
    scene_passed = models.BooleanField(default = False)
    def __str__(self):
        return self.video_title

class Inspection_vote(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    qualified = models.BooleanField(default = False)
    end_time = models.DateTimeField(default = datetime.datetime.now)
    start_time = models.DateTimeField(default = datetime.datetime.now)
    batch_id = models.CharField(max_length = 200, default = "")
    w_id = models.CharField(max_length=200, default = "")
    class Meta:
        abstract = True


class Video_quality_inspection_vote(Inspection_vote):
    def __str__(self):
        return self.video.video_title

class Sound_quality_inspection_vote(Inspection_vote):
    def __str__(self):
        return self.video.video_title

class Language_inspection_vote(Inspection_vote):
    def __str__(self):
        return self.video.video_title

class Conversation_inspection_vote(Inspection_vote):
    def __str__(self):
        return self.video.video_title

class Scene_inspection_vote(Inspection_vote):
    def __str__(self):
        return self.video.video_title
