from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Video_Before_Processing)
admin.site.register(Experiment_Video)
admin.site.register(Emotion_label_experiment)
admin.site.register(Emotion_check_experiment)
admin.site.register(Emotion_Label_Component_Process)
admin.site.register(Emotion_Label_Component_Process_Likert)
admin.site.register(Emotion_Label_Baseline)
admin.site.register(Emotion_Label_Component_Process_Only)
admin.site.register(Emotion_Distribution_Collection)
admin.site.register(Emotion_Distribution_Example)
