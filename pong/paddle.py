"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  
"""
from pygame import Rect

from pong.object import GameObject

class Paddle(GameObject):
    """
    Author:       Kyle Lastimosa
    Purpose:     
    Pre:         
    Post:        
    """ 
    def __init__(self, rect: Rect) -> None:
        """
        Author:       Kyle Lastimosa
        Purpose:     
        Pre:         
        Post:        
        """ 
        super().__init__(rect)
