from django import forms
from models import *
from crispy_forms.helper import FormHelper

from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    # declare the fields you will show
    username = forms.CharField(label="Your Username")
    # first password field
    password1 = forms.CharField(label="Your Password",widget=forms.PasswordInput)
    # confirm password field
    password2 = forms.CharField(label="Repeat Your Password",widget=forms.PasswordInput)
    email = forms.EmailField(label = "Email Address")
 
    # this sets the order of the fields
    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2", )
 
    # this redefines the save function to include the fields you added
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

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
