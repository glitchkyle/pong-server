"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """
    Author:       Kyle Lastimosa
    Purpose:     
    Pre:         
    Post:        
    """ 
    def create_user(self, username, password=None, **extra_fields):
        """
        Author:       Kyle Lastimosa
        Purpose:     
        Pre:         
        Post:        
        """ 
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Author:       Kyle Lastimosa
        Purpose:     
        Pre:         
        Post:        
        """ 
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    """
    Author:       Kyle Lastimosa
    Purpose:     
    Pre:         
    Post:        
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
        Author:       Kyle Lastimosa
        Purpose:     
        Pre:         
        Post:        
        """ 
        return self.username

    def has_perm(self, perm, obj=None):
        """
        Author:       Kyle Lastimosa
        Purpose:     
        Pre:         
        Post:        
        """ 
        return self.is_superuser

    def has_module_perms(self, app_label):
        """
        Author:       Kyle Lastimosa
        Purpose:     
        Pre:         
        Post:        
        """ 
        return self.is_superuser