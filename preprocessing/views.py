from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .forms import *
from .video_url_accumulate import *
from .task_management import *
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

def video_quality_inspection(request, criteria):
    select_field()
    return render(request, "video_quality_inspection.html", {'criteria': criteria})
