from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def search_and_accumulate_url(request):
    return render(request, "search_and_accumulate_url.html", {})

def video_quality_inspection(request):
    return render(request, "video_quality_inspection.html", {})
