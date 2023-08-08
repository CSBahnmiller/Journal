from django import forms
from django.contrib.auth.forms import UserCreationForm
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
        fields = ( "title", "mood", "feeling", "content")
