from django import forms

class EmotionResult(forms.Form):
    to_return = forms.CharField()
