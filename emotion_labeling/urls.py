from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^character_time_designator/(?P<title>[\w\-]+)/$', views.character_time_designator),
    #label and reason
    url(r'^experiment1_baseline/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1_baseline),
    url(r'^experiment1_distribution/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1_distribution),
    url(r'^experiment1_distribution_tutolike_ED_tutorial/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1_distribution_tutolike_ED_tutorial),
    url(r'^experiment1_distribution_tutolike_ED/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1_distribution_tutolike_ED),
    url(r'^experiment1_distribution_adaptive_ED/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1_distribution_adaptive_ED),
    #for component_process condition
    url(r'^experiment1_cp/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1_cp),
    url(r'^experiment1_cp_prescreening/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1_cp_prescreening),
    #for component_process condition
    url(r'^experiment1_cp_likert/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1_cp_likert),
    url(r'^experiment1_cp_only/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1_cp_only),
    url(r'^emotion_task_deploy/$', views.emotion_task_deploy),
    url(r'^bonus_for_hits/(?P<hit>[\w\-]+)/$', views.bonus_for_hits),
#    url(r'^video_quality_inspection/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.video_quality_inspection),

]
