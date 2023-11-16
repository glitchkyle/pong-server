"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  To register the User model with the Django admin site.
ChatGPT generated some of these comments for the function
"""
from django.contrib import admin

from .models import User

admin.site.register(User)
