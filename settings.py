from dataclasses import dataclass, field
from math import ceil
from typing import Optional
from PyQt6.QtGui import QColor


@dataclass
class Settings:
    SCREEN_WIDTH: int
    SCREEN_HEIGHT: int
    CELL_WIDTH: int = 8
    CELL_HEIGHT: int = 8
    SCREEN_BACKGROUND = QColor(66, 135, 245)
    CELL_ALIVE_COLOR = QColor(0, 0, 0)
    CELL_DEAD_COLOR = QColor(66, 135, 245)
    N_CELLS_HORIZONTAL: Optional[int] = None
    N_CELLS_VERTICAL: Optional[int] = None
    N_CELLS: Optional[int] = None

    def __post_init__(self):
        self.N_CELLS_HORIZONTAL = ceil(self.SCREEN_WIDTH / self.CELL_WIDTH)
        self.N_CELLS_VERTICAL = ceil(self.SCREEN_HEIGHT / self.CELL_HEIGHT)
        self.N_CELLS = self.N_CELLS_HORIZONTAL * self.N_CELLS_VERTICAL
