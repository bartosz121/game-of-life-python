from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QColor, QPainter, QBrush

from grid_object import GridObject


class Cell(GridObject):
    __slots__ = (
        "_x",
        "_y",
        "_width",
        "_height",
        "_is_alive",
        "_alive_color",
        "_dead_color",
        "alive_neighbours",
        "color",
    )

    def __init__(self, x, y, width, height, alive_color, dead_color):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._is_alive = False
        self._alive_color = alive_color
        self._dead_color = dead_color
        self.alive_neighbours = 0
        self.color = dead_color

    def __repr__(self):
        args = (
            str(a)
            for a in (
                self.x,
                self.y,
                self._width,
                self._height,
                self._alive_color,
                self._dead_color,
            )
        )
        return f"Cell({', '.join(args)})"

    def __str__(self):
        return (
            f"Cell(x={self.x}, y={self.y}, is_alive={self.is_alive},"
            f" alive_neighbours={self.alive_neighbours}, color={self.color})"
        )

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def is_alive(self):
        return self._is_alive

    @is_alive.setter
    def is_alive(self, state: bool):
        self._is_alive = state
        self._set_correct_color()

    def _set_correct_color(self):
        if self._is_alive:
            self.color = self._alive_color
        else:
            self.color = self._dead_color

    def draw(self, painter: QPainter):
        painter.setBrush(QBrush(self.color))
        painter.drawRect(self._x, self._y, self._width, self._height)
