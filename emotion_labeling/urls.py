from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^experiment1/$', views.experiment1),
#    url(r'^video_quality_inspection/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.video_quality_inspection),

]
