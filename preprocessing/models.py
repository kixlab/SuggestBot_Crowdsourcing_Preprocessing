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

class Video_quality_inspection_vote(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    video_quality = models.BooleanField(default = False)
    start_time = models.DateTimeField(default = datetime.datetime.now())
    end_time = models.DateTimeField(default = datetime.datetime.now())
    batch_id = models.CharField(max_length = 200, default = "")
    def __str__(self):
        return self.video.video_title

class Sound_quality_inspection_vote(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    sound_quality = models.BooleanField(default = False)
    start_time = models.DateTimeField(default = datetime.datetime.now())
    end_time = models.DateTimeField(default = datetime.datetime.now())
    batch_id = models.CharField(max_length = 200, default = "")
    def __str__(self):
        return self.video.video_title

class Language_inspection_vote(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    language = models.BooleanField(default = False)
    start_time = models.DateTimeField(default = datetime.datetime.now())
    end_time = models.DateTimeField(default = datetime.datetime.now())
    batch_id = models.CharField(max_length = 200, default = "")
    def __str__(self):
        return self.video.video_title

class Conversation_inspection_vote(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    conversation = models.BooleanField(default = False)
    start_time = models.DateTimeField(default = datetime.datetime.now())
    end_time = models.DateTimeField(default = datetime.datetime.now())
    batch_id = models.CharField(max_length = 200, default = "")
    def __str__(self):
        return self.video.video_title

class Scene_inspection_vote(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    scene = models.BooleanField(default = False)
    start_time = models.DateTimeField(default = datetime.datetime.now())
    end_time = models.DateTimeField(default = datetime.datetime.now())
    batch_id = models.CharField(max_length = 200, default = "")
    def __str__(self):
        return self.video.video_title
