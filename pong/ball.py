from pygame import Rect
from random import sample

from config.constants import BALL_SPEED
from pong.object import GameObject


class Ball(GameObject):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)

        speeds: set[int] = set([-BALL_SPEED, BALL_SPEED])
        start_x_vel = sample(speeds, 1)[0]
        start_y_vel = sample(speeds, 1)[0]
        self.velocity = (start_x_vel, start_y_vel)

    def update(self, rect: Rect, velocity: tuple[int, int]):
        super().update(rect)
        self.velocity = velocity
