"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  Establishes a custom user model with a manager to support user creation and superuser creation.
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """
    Author:       Kyle Lastimosa, James.Chen
    Purpose:      Provides helper functions to create User or superuser instances. 
    Pre:          None
    Post:         UserManager is ready to create user instances.
    """ 
    def create_user(self, username, password=None, **extra_fields):
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      Creates a standard user with a username and password.
        Pre:          A username must be provided; password and extra_fields are optional.
        Post:         A User instance is created and saved to the database.
        """ 
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      Creates a superuser with admin rights.
        Pre:          A username and password must be provided; extra_fields can override default admin settings.
        Post:         A superuser instance is created and saved to the database.
        """ 
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    """
    Author:       Kyle Lastimosa, James Chen
    Purpose:      Custom User model to support additional game-related attributes.
    Pre:          None
    Post:         A User model is available for representing users in the database.
    """ 
    username = models.CharField(max_length=150, unique=True)
    games = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      To return the username as a string representation of the User.
        Pre:          A User instance must exist.
        Post:         The username string is returned.
        """ 
        return self.username

    def has_perm(self, perm, obj=None):
        """
        Author:       Kyle Lastimosa
        Purpose:      To determine if the user has a specific permission.
        Pre:          'perm' is a string naming a permission.
        Post:         Returns True if the user is a superuser, otherwise false.
        """ 
        return self.is_superuser

    def has_module_perms(self, app_label):
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      To determine if the user has permissions for a given app.
        Pre:          'app_label' is the name of the app.
        Post:         Returns True if the user is a superuser, otherwise false.
        """ 
        return self.is_superuser