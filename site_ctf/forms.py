from django import forms
from models import *
from crispy_forms.helper import FormHelper

class ValidationForm(forms.Form):
    flagID = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    flagValue = forms.CharField(max_length=100, label="Flag", required=True)
    
    def __init__(self, *args, **kwargs):
        challID = kwargs.pop('idChall', None)
        super(ValidationForm, self).__init__(*args, **kwargs)
        if challID:
            self.fields['flagID'].initial=challID
        return

    def validateFlag(self):
        chall = Challenge.objects.get(id=self.cleaned_data.get('flagID'))
        if chall.flag==self.cleaned_data.get('flagValue'): 
            return True
        else:
            return False

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
