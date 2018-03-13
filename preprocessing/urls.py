from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search_and_accumulate_url/$', views.search_and_accumulate_url),
    url(r'^video_quality_inspection/(?P<wid>[\w\-]+)/(?P<aid>[\w\-]+)/$', views.video_quality_inspection),

]
