from pygame import Rect
from random import randint

from config.constants import BALL_SPEED

class Ball(object):
    def __init__(self, rect: Rect) -> None:
        self.rect = rect
        self.start_rect = rect
        self.velocity = (randint(-BALL_SPEED, BALL_SPEED), randint(-BALL_SPEED, BALL_SPEED))