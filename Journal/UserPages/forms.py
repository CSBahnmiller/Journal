from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserContent



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "password1", "password2"]


class UserContentForm(forms.ModelForm):
    class Meta:
        model = UserContent
        fields = ( "title", "mood", "feeling", "graditude",  "content")


class PasswordChangingFrom(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    class Meta:
        model = User
        fields = ("old_password","new_password1","new_password2")

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    class Meta:
        model = User
        feilds = ("username", "password")