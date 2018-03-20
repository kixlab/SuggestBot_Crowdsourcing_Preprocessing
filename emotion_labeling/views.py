from django.shortcuts import render

# Create your views here.
def experiment1(request):

    return render(request, "emotion_labeling_task.html", {})
