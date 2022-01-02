import sys
from abc import abstractmethod
from PyQt6.QtGui import QPainter, QBrush
from typing import Protocol

from gui import game_window


class GameObject(Protocol):
    def draw(self, painter: QPainter, brush: QBrush):
        """Draw the object"""


class Game:
    def __init__(
        self, title: str, width: int, height: int, *, timer_interval: int = 100
    ):
        self.title = title
        self.running = False
        # pyqt6
        self.app = game_window.LoggerApplication([])
        self.window = game_window.GameWindow(
            title, width, height, timer_interval=timer_interval
        )

    def initialize_game(self):
        self.running = True
        self.window.timer.timeout.connect(self.run)  # invoke self.run on each iteration
        self.window.timer.start()
        self.window.show()
        sys.exit(self.app.exec())

    @abstractmethod
    def run(self):
        ...
