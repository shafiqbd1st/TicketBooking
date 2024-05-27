from django import forms
from .models import Train, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["name", "body"]


class ChangeUserData(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
