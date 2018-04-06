from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^in_lab/(?P<video_title>[\w\-]+)/$', views.in_lab),
    #label and reason
    url(r'^experiment1/(?P<condition>[\w\-]+)/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1),
    #for component_process condition
    url(r'^experiment1_cp/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1_cp),
    url(r'^experiment1_cp_prescreening/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1_cp_prescreening),
    #for component_process condition
    url(r'^experiment1_cp_likert/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment1_cp_likert),
    #sanity check
    url(r'^experiment2/(?P<video_title>[\w\-]+)/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.experiment2),
#    url(r'^video_quality_inspection/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.video_quality_inspection),

]
