from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .forms import *
from .video_url_accumulate import *
from .task_management import *
from .socket_management import *
import json
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import numpy as np
import cv2
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

def search_and_accumulate_url(request):
    send_url("dorothy")
    if request.method=="POST":
        print("!")
        form = SearchKeyword(request.POST)
        if form.is_valid():
            keyword = json.loads(form.cleaned_data['video_keyword'])
            vid_num = form.cleaned_data['video_num']
            accumulated_num = video_search_and_accumulate(keyword, vid_num)
            print(keyword)
            return HttpResponse("Successfully accumulated "+str(accumulated_num)+" video ids")
    return render(request, "search_and_accumulate_url.html", {})

def video_quality_inspection(request, wid, aid):
    if request.method=="POST":
        print("heyheyhey")
        form = InspectionResult(request.POST)
        if form.is_valid():
            to_return = json.loads(form.cleaned_data['to_return'])
            token = isp_store_result(to_return, wid, aid)
            token = {'token': token}
            return render(request, "token_return.html", token)

    isp_remove_outdated_tasks()
    task_to_throw = isp_select_field(wid, aid)

    return render(request, "video_quality_inspection.html", task_to_throw)

def inspection_test(request):
    if request.method=="POST":
        form = InspectionResult(request.POST)
        print(form)
        to_return = json.loads(form.cleaned_data['to_return'])
        criteria = to_return['criteria']
        return render(request, "token_return.html", {'token':"Thank you for testing it! When writing feedback in the coffee time doc, please write '"+criteria+"' next to your name!"})

    task_to_throw = test_deployer()

    return render(request, "video_quality_inspection.html", task_to_throw)

# below view function receives post request from external client
#specifically, it receives image data and store it into the designated path
@require_http_methods(['POST'])
@csrf_exempt
def receive_facial_result(request):
    if request.method=="POST":
        print("heh")
        data = request.FILES['media']
        #need to decide where to store the file...
        path = default_storage.save('img.png', ContentFile(data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)

    return render(request, 'search_and_accumulate_url.html')
