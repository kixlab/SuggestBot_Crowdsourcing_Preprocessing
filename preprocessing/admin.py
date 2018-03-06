from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Video)
admin.site.register(Video_quality_inspection_vote)
admin.site.register(Sound_quality_inspection_vote)
admin.site.register(Language_inspection_vote)
admin.site.register(Conversation_inspection_vote)
admin.site.register(Scene_inspection_vote)
