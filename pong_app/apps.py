"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  Defines the configuration for the pong_app Django application. 
ChatGPT generated some of these comments for the function
"""
from django.apps import AppConfig

class PongAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pong_app"
