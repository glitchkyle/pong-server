"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  Defines the URL pattern for the index view of the web application.
ChatGPT generated some of these comments for the function
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]