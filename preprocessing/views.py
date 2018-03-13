from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .forms import *
from .video_url_accumulate import *
from .task_management import *
import json

def search_and_accumulate_url(request):
    if request.method=="POST":
        print("!")
        form = SearchKeyword(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['video_keyword']
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
            isp_store_result(to_return)

    isp_remove_outdated_tasks()
    task_to_throw = isp_select_field(wid, aid)

    return render(request, "video_quality_inspection.html", task_to_throw)
