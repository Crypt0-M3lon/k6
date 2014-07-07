from django import forms
from models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from crispy_forms.bootstrap import PrependedText
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserCreateForm(UserCreationForm):
    helper = FormHelper()
    helper.form_tag = True
    helper.form_show_labels = False
    helper.help_text_inline = True
    helper.add_input(Submit('submit', 'Go!'))
    helper.layout = Layout(

      # declare the fields you will show
      Field('username', placeholder="Nom d'utilisateur"),
      # first password field
      Field('password1', placeholder="Mot de passe"),
      # confirm password field
      Field('password2',placeholder="Confirmez votre mot de passe"),
    
      PrependedText('email','@',placeholder="E-mail")
    )
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

class UserEditProfile(UserChangeForm):
    helper = FormHelper()
    helper.form_tag = True
    helper.form_show_labels = True
    helper.help_text_inline = True
    helper.add_input(Submit('submit', 'Modifier'))
    helper.layout = Layout(
      
    Field('username', label="Nom d'utilisateur :"),
    Field('email',label="E-mail"),
    Field('is_staff', label="Statut : "),
    Field('is_active', label="Actif ou pas ?"),
    Field('password', type="hidden"),

    )
    # this sets the order of the fields
    class Meta:
        model = User
        fields = ("email", "username", "password","is_staff", "is_active")
 
    # this redefines the save function to include the fields you added
    def save(self, commit=True):
        user = super(UserEditProfile, self).save(commit=False)
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
