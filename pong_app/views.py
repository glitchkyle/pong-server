from django.contrib.auth import login, authenticate

from django.shortcuts import render
from .models import User
from .forms import UserRegistrationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def index(request):
    user_list = User.objects.all()
    context = {"user_list": user_list}
    return render(request, "pong_app/index.html", context)

class AuthenticationView(APIView):
    def post(self, request, format=None):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Authentication successful
            return Response({'message': 'Authentication successful'}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'message': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return index(request)  # Redirect to a success page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})