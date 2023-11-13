"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  
"""
from django.contrib.auth import authenticate

from django.shortcuts import render
from .models import User
from .forms import UserRegistrationForm

def index(request):
    """
    Author:       Kyle Lastimosa
    Purpose:     
    Pre:         
    Post:        
    """ 
    user_list = User.objects.all()
    context = {"user_list": user_list}
    return render(request, "pong_app/index.html", context)

def authenticationUser(player_credentials):
    """
    Author:       Kyle Lastimosa
    Purpose:     
    Pre:         
    Post:        
    """ 
    user = authenticate(username=player_credentials['username'], password=player_credentials['password'])
    if user is not None:
        return True
    else:
        return False

def register_user(player):
    """
    Author:       Kyle Lastimosa
    Purpose:     
    Pre:         
    Post:        
    """ 
    player_credentials = {
        "username": player['username'],
        "password1": player['password'],
        "password2":player['confirm_password']
    }
    
    form = UserRegistrationForm(player_credentials)
    if form.is_valid():
        user = form.save()
        return authenticationUser(player)
    else:
        return False
