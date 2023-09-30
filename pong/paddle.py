from pygame import Rect

class Paddle(object):
    def __init__(self, rect: Rect) -> None:
        self.rect = rect
        self.startRect = rect
    
    def update(self, rect: Rect) -> None:
        self.rect = rect
    
    def reset(self) -> None:
        self.rect = self.startRect