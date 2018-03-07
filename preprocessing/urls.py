from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search_and_accumulate_url/$', views.search_and_accumulate_url),
    url(r'^video_quality_inspection/$', views.video_quality_inspection),

]
