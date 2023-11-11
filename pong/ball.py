from pygame import Rect
from random import randint

from config.constants import BALL_SPEED
from pong.object import GameObject


class Ball(GameObject):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)
        self.reset()

    def reset(self) -> None:
        super().reset()

        speeds = [-BALL_SPEED, BALL_SPEED]
        n = len(speeds)
        start_x_vel = speeds[randint(0, n-1)]
        start_y_vel = speeds[randint(0, n-1)]
        self.velocity = (start_x_vel, start_y_vel)

    def update(self, rect: Rect, velocity: tuple[int, int]):
        super().update(rect)
        self.velocity = velocity
