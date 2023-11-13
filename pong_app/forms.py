"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  
"""
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserRegistrationForm(UserCreationForm):
    """
    Author:       Kyle Lastimosa
    Purpose:     
    Pre:         
    Post:        
    """ 
    class Meta:
        model = User
        fields = ['username']
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(render_value=False)
    )