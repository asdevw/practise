from django import forms
from .models import *



class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = '__all__'



class EmailForm(forms.Form):
    recipient = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)