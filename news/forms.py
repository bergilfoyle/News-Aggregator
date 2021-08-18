from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from news.models import Source, UserSource
from django.forms import ModelForm


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class UserDetailsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserDetailsForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Email')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username).exclude(pk=self.user.id)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email).exclude(pk=self.user.id)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        obj, created = User.objects.get_or_create(username = self.user.username)
        obj.username = self.cleaned_data['username']
        obj.email = self.cleaned_data['email']
        obj.save()
        return obj


class SourcesForm(forms.Form):
    currentuser, checked = None, None
    def __init__(self, *args, **kwargs):
        self.__class__.currentuser = kwargs.pop('user', None)
        obj, created = UserSource.objects.get_or_create(current_user = self.__class__.currentuser)
        self.__class__.checked = kwargs.pop('checked', None)
        super(SourcesForm, self).__init__(*args, **kwargs)
    
    sources = forms.ModelMultipleChoiceField(required = False, queryset = Source.objects.all(), widget  = forms.CheckboxSelectMultiple())

    def save(self, commit=True):
        obj = UserSource.updatesources(self.__class__.currentuser, self.__class__.checked)
        return obj
