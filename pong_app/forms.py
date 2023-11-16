"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  To define a user registration form that inherits from Django's default UserCreationForm.
ChatGPT generated some of these comments for the function
"""
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserRegistrationForm(UserCreationForm):
    """
    Author:       Kyle Lastimosa
    Purpose:      Customizes user registration to include username and password.
    Pre:          None
    Post:         Form is ready to render and process user registration data.
    """ 
    class Meta:
        model = User
        fields = ['username']
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(render_value=False)
    )