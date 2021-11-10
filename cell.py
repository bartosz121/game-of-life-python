from pygame import Rect
from settings import (
    BASIC_COLORS,
    CELL_DEFAULT_COLOR,
    CELL_WIDTH,
    CELL_HEIGHT,
    SCREEN_BACKGROUND,
)


class Cell:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._is_alive = False
        self._rect = Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
        self.alive_neighbours = 0
        self.color = CELL_DEFAULT_COLOR.rgb

    def __repr__(self):
        return f"Cell({self.x!r}, {self.y!r})"

    def __str__(self):
        return (
            f"Cell({self.x}, {self.y}, is_alive={self.is_alive},"
            f" alive_neighbours={self.alive_neighbours}, color={self.color})"
        )

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def rect(self):
        return self._rect

    @property
    def is_alive(self):
        return self._is_alive

    @is_alive.setter
    def is_alive(self, state: bool):
        # if cell is alive change color to black if not to background color
        if state:
            self.color = BASIC_COLORS["BLACK"]
        else:
            self.color = SCREEN_BACKGROUND
        self._is_alive = state
