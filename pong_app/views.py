from django.contrib.auth import authenticate

from django.shortcuts import render
from .models import User
from .forms import UserRegistrationForm

def index(request):
    user_list = User.objects.all()
    context = {"user_list": user_list}
    return render(request, "pong_app/index.html", context)

def authenticationUser(player_credentials):

    user = authenticate(username=player_credentials['username'], password=player_credentials['password'])
    if user is not None:
        return True
    else:
        return False

def register_user(player):
    
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
