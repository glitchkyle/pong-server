"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  This file defines the Ball class, which represents the game ball in a Pong-like game. 
                          It includes methods for initializing, resetting, and updating the ball's position and velocity.
ChatGPT generated some of these comments for the function                        
"""
from pygame import Rect
from random import randint

from config.constants import BALL_SPEED
from pong.object import GameObject
      
class Ball(GameObject):
    """
    Author:       Kyle Lastimosa, James Chen
    Purpose:      Represents the game ball, inheriting from GameObject.
    Pre:          The GameObject class must be defined.
    Post:         An instance of the Ball class is created with the specified rectangle.     
    """ 
    def __init__(self, rect: Rect) -> None:
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      Initializes the Ball object with the given rectangle and resets its state.
        Pre:          The GameObject class must be defined.
        Post:         The Ball object is initialized with the specified rectangle, and its state is reset.
        """ 
        super().__init__(rect)
        self.reset()

    def reset(self) -> None:
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      Resets the state of the ball, including its position and velocity.
        Pre:          The Ball object must be initialized.
        Post:         The Ball object's state is reset, and it is ready for a new round.
        """     
        super().reset()

        speeds = [-BALL_SPEED, BALL_SPEED]
        n = len(speeds)
        start_x_vel = speeds[randint(0, n-1)]
        start_y_vel = speeds[randint(0, n-1)]
        self.velocity = (start_x_vel, start_y_vel)

    def update(self, rect: Rect, velocity: tuple[int, int]):
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      Updates the position and velocity of the ball.
        Pre:          The Ball object must be initialized.
        Post:         The Ball object's position and velocity are updated based on the given parameters.
        """ 
        super().update(rect)
        self.velocity = velocity
