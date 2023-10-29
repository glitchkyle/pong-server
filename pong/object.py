from pygame import Rect

TupleRect = tuple[int, int, int, int]


class GameObject(object):
    def __init__(self, rect: Rect) -> None:
        self.rect = rect
        self.startRect = rect

    def __str__(self) -> None:
        return f"({self.rect[0]}, {self.rect[1]})"

    def to_tuple_rect(self) -> TupleRect:
        return (self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def update(self, rect: Rect) -> None:
        self.rect = rect

    def reset(self) -> None:
        self.rect = self.startRect
