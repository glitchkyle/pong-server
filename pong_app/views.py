"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  To provide views for user authentication and registration within the pong_app application.
ChatGPT generated some of these comments for the function
"""
from django.contrib.auth import authenticate

from django.shortcuts import render
from .models import User
from .forms import UserRegistrationForm

def index(request):
    """
    Author:       Kyle Lastimosa, James Chen
    Purpose:      Display the homepage with a list of users.
    Pre:          HTTP request received.
    Post:         Renders the index page with user context.
    """ 
    user_list = User.objects.all()
    context = {"user_list": user_list}
    return render(request, "pong_app/index.html", context)

def authenticationUser(player_credentials):
    """
    Author:       Kyle Lastimosa, James Chen
    Purpose:      Authenticate a user based on provided credentials.
    Pre:          'player_credentials' dictionary with 'username' and 'password'.
    Post:         Returns True if authentication succeeds, False otherwise.
    """ 
    user = authenticate(username=player_credentials['username'], password=player_credentials['password'])
    if user is not None:
        return True
    else:
        return False

def register_user(player):
    """
    Author:       Kyle Lastimosa
    Purpose:      Register a new user using the provided player data.
    Pre:          'player' dictionary with 'username', 'password', and 'confirm_password'.
    Post:         Returns True if registration and authentication succeed, False otherwise.
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
