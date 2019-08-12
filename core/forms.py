from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Pet, Profile, Contact
from django.forms import ModelForm
import datetime
from crispy_forms.layout import Layout, Submit, Row, Column
from functools import partial

class UserForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['sitter'].queryset = Contact.objects.filter(user=user)

    sitter = forms.ModelChoiceField(queryset=None, widget=forms.Select, required=True)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class ProfileUpdateForm(forms.Form):
    homephone= forms.CharField(max_length=10)
    mobilephone = forms.CharField(max_length=10)
    workphone = forms.CharField(max_length=10)



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','phone','work_phone',]

  

class ChecklistForm(forms.Form):
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    task1 = forms.CharField(max_length=300, required=False)
    task2 = forms.CharField(max_length=300, required=False)
    task3 = forms.CharField(max_length=300, required=False)
    task4 = forms.CharField(max_length=300, required=False)
    task5 = forms.CharField(max_length=300, required=False)
    task6 = forms.CharField(max_length=300, required=False)
    task7 = forms.CharField(max_length=300, required=False)
    task8 = forms.CharField(max_length=300, required=False)
    task9 = forms.CharField(max_length=300, required=False)
    task10 = forms.CharField(max_length=300, required=False)

class ChecklistForm2(forms.Form):
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
   

"""Create a new animal profile."""
class AddAPetForm(forms.ModelForm):
    class Meta:
        model = Pet
        exclude = ['owner']
        fields = ('name','animal','profile_Image','breed','weight_in_lbs','sex','color_and_Markings','age', 'about_Me','vet_Info','emergency_Contact')

class ProfileSearch(forms.Form):
    user_search = forms.CharField(max_length=300, required=False, help_text="Use this form to search for another user's profile page. From there, you can add them to your contacts.")
