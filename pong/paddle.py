from pygame import Rect

from pong.object import GameObject


class Paddle(GameObject):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)
