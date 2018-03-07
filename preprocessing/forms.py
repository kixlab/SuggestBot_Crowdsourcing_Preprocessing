from django import forms

class SearchKeyword(forms.Form):
    video_keyword = forms.CharField()
    video_num = forms.IntegerField()

class InspectionResult(forms.Form):
    to_return = forms.CharField()