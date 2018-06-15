from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^study_frame_checkbox_confidence/(?P<data_name>[\w\-]+)/$', views.study_frame_checkbox_confidence),
    url(r'^interface_study_arousal_valence/(?P<data_name>[\w\-]+)/$', views.interface_study_arousal_valence),
    url(r'^interface_study_emotion_word/(?P<data_name>[\w\-]+)/$', views.interface_study_emotion_word),
    url(r'^interface_study_frame_disambiguation/(?P<data_name>[\w\-]+)/$', views.interface_study_frame_disambiguation),
    url(r'^interface_study_student_engagement/(?P<data_name>[\w\-]+)/$', views.interface_study_student_engagement),
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
    url(r'^emotion_task_deploy_distribution/(?P<pass_word>[\w\-]+)/$', views.emotion_task_deploy_distribution),
    url(r'^bonus_for_hits/(?P<hit>[\w\-]+)/$', views.bonus_for_hits),
    url(r'^build_examples_from_collected_data/$', views.build_examples_from_collected_data),
    url(r'^extract_similar_examples/$', views.extract_similar_examples),
#    url(r'^video_quality_inspection/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.video_quality_inspection),

]
