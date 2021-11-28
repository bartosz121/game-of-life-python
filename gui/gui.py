from collections.abc import Iterable
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QGridLayout, QWidget
from typing import Protocol


class GameObject(Protocol):
    def draw(self, painter: QtGui.QPainter, brush: QtGui.QBrush):
        """Draw the object"""


class LoggerApplication(QApplication):

    t = QtCore.QElapsedTimer()

    def notify(self, receiver, event):
        self.t.start()
        ret = QApplication.notify(self, receiver, event)
        if self.t.elapsed() > 10:
            print(
                f"processing event type {event.type()} for object {receiver.objectName()} "
                f"took {self.t.elapsed()}ms"
            )
        return ret


class GameWindow(QWidget):
    def __init__(
        self,
        title: str,
        width: int,
        height: int,
        *,
        timer_interval: int,
    ):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(width, height)
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # timer is used for performing some action periodically in the application
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(timer_interval)
