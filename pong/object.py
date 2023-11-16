"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  Manages the properties and state of a game object.      
"""
from pygame import Rect

TupleRect = tuple[int, int, int, int]

class GameObject(object):
    """
    Author:       Kyle Lastimosa
    Purpose:      Base class for game objects with a rectangular shape. 
    Pre:          None 
    Post:         GameObject instance is created with initial position and size.
    """ 
    def __init__(self, rect: Rect) -> None:
        """
        Author:       Kyle Lastimosa
        Purpose:      Initializes a new game object with a rectangle defining its position and size.
        Pre:          A pygame.Rect object is provided.
        Post:         GameObject instance is created with the specified rectangle.
        """ 
        self.rect = rect
        self.startRect = rect
 
    def __str__(self) -> None:
        """
        Author:       Kyle Lastimosa
        Purpose:      Provide representation of a game object's position.
        Pre:          GameObject instance exits.
        Post:         Returns a string representing the object's current position.
        """ 
        return f"({self.rect[0]}, {self.rect[1]})"

    def to_tuple_rect(self) -> TupleRect:
        """
        Author:       Kyle Lastimosa
        Purpose:      Converts the GameObject's rectangle to a tuple.
        Pre:          GameObject instance exists with a defined rectangle.
        Post:         Returns a tuple with the position and size of the rectangle.
        """ 
        return (self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def update(self, rect: Rect) -> None:
        """
        Author:       Kyle Lastimosa
        Purpose:      Updates the GameObject's position and size to a new rectangle.
        Pre:          A new pygame.Rect object is provided.
        Post:         The GameObject's rectangle is updated to the new position and size.
        """ 
        self.rect = rect
 
    def reset(self) -> None:
        """
        Author:       Kyle Lastimosa
        Purpose:      Resets the GameObject's position and size to its initial state.
        Pre:          GameObject instance exists and has a defined starting rectangle.
        Post:         The GameObject's rectangle is reset to its original position and size.
        """ 
        self.rect = self.startRect
