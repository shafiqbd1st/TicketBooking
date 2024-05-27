from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from Train import models


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"id": "required"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"id": "required"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"id": "required"}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit == True:
            our_user.is_active = False
            our_user.save()
            models.UserProfile.objects.create(user=our_user)
        return our_user


class depositForm(forms.Form):
    amount = forms.IntegerField(label="Amount", required=True)
