from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(render_value=False)
    )