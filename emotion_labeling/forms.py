from django import forms

class EmotionResult(forms.Form):
    to_return = forms.CharField()

class DistributionResult(forms.Form):
    to_return = forms.CharField()
    start_time = forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M"])
