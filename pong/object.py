"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  
"""
from pygame import Rect

TupleRect = tuple[int, int, int, int]

class GameObject(object):
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
        self.rect = rect
        self.startRect = rect
 
    def __str__(self) -> None:
        """
        Author:       Kyle Lastimosa
        Purpose:     
        Pre:         
        Post:        
        """ 
        return f"({self.rect[0]}, {self.rect[1]})"

    def to_tuple_rect(self) -> TupleRect:
        """
        Author:       Kyle Lastimosa
        Purpose:     
        Pre:         
        Post:        
        """ 
        return (self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def update(self, rect: Rect) -> None:
        """
        Author:       Kyle Lastimosa
        Purpose:     
        Pre:         
        Post:        
        """ 
        self.rect = rect
 
    def reset(self) -> None:
        """
        Author:       Kyle Lastimosa
        Purpose:     
        Pre:         
        Post:        
        """ 
        self.rect = self.startRect
