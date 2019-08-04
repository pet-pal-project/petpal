from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Pet, Profile
from django.forms import ModelForm
import datetime
from crispy_forms.layout import Layout, Submit, Row, Column
from functools import partial


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


from django import forms


class ProfileUpdateForm(forms.Form):
    homephone= forms.CharField(max_length=10)
    mobilephone = forms.CharField(max_length=10)
    workphone = forms.CharField(max_length=10)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['home_phone','mobile_phone','work_phone']

  

class ChecklistForm(forms.Form):
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})
    sitter = forms.CharField(max_length=50)
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    task1 = forms.CharField(max_length=300)
    task2 = forms.CharField(max_length=300)
    task3 = forms.CharField(max_length=300)
    task4 = forms.CharField(max_length=300)
    task5 = forms.CharField(max_length=300)