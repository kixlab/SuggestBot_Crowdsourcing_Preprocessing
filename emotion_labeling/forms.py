from django import forms

class EmotionResult(forms.Form):
    to_return = forms.CharField()

class DistributionResult(forms.Form):
    to_return = forms.CharField()
    start_time = forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M"])

class TaskDeployResult(forms.Form):
    to_return = forms.CharField()
    hit_num = forms.IntegerField()

class FrameStudyResult(forms.Form):
    frame_confidences = forms.CharField()
    no_field_reasoning = forms.CharField()

class SurveyResult(forms.Form):
    survey_result = forms.CharField()
