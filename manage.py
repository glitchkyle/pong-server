#!/usr/bin/env python
"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  Executes the Django application 
ChatGPT generated some of these comments for the function
"""
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """
    Author:       Kyle Lastimosa, James Chen
    Purpose:      Start the Django application server for administrative tasks. 
    Pre:          Django installed, environment variables set, virtual environment activated if required.
    Post:         Django server is running and ready for commands or HTTP requests.
    """ 
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pong_game.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
