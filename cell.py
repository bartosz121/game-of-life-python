from pygame import Rect
from color import Color
from settings import (
    BASIC_COLORS,
    CELL_DEFAULT_COLOR,
    CELL_WIDTH,
    CELL_HEIGHT,
    SCREEN_BACKGROUND,
)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._color = CELL_DEFAULT_COLOR.rgb
        self._is_alive = False
        self._num_neighbors = 0
        # pygame.Rect(left, top, width, height)
        # pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
        self.rect = Rect(x, y, CELL_WIDTH, CELL_HEIGHT)

    def __repr__(self):
        return (
            f"============================\n"
            f"\tCell({self.x}, {self.y})\n"
            f"\tisAlive: {self.is_alive}\n"
            f"\tNeighbors(Alive): {self.num_neighbors}\n"
            f"\tColor: {self.color}\n"
            f"============================"
        )

    def check_position(self):
        return f"({self.x}, {self.y})"

    @property
    def num_neighbors(self):
        return self._num_neighbors

    @num_neighbors.setter
    def num_neighbors(self, n):
        self._num_neighbors = n

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

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color: Color):
        self._color = new_color.rgb
