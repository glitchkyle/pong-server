"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  Extension of GameObject to represent a paddle in the game.
ChatGPT generated some of these comments for the function 
"""
from pygame import Rect

from pong.object import GameObject

class Paddle(GameObject):
    """
    Author:       Kyle Lastimosa, James Chen
    Purpose:      Represents a player's paddle in the game, extending GameObject.
    Pre:          None
    Post:         Paddle instance is created with a position and size.
    """ 
    def __init__(self, rect: Rect) -> None:
        """
        Author:       Kyle Lastimosa, James Chen, Nishan Budhathoki
        Purpose:      Initializes a paddle with a given rectangle.
        Pre:          'rect' is a valid pygame.Rect instance.
        Post:         Paddle instance is initialized and ready for game logic.
        """ 
        super().__init__(rect)
