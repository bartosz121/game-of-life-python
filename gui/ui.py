from abc import abstractmethod
from PyQt6 import QtCore
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from typing import Generator, Any


class Communicator(QtCore.QObject):
    """Responsible for sending signals from UI to game window"""

    btn_clicked = QtCore.pyqtSignal(str)


class UIBuilder:
    """
    UIBuilder

    Every UI element should be named with 'ui_' prefix
    """

    def __init__(self) -> None:
        self._ui_elements: list[QWidget] = list()

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name.startswith("ui_"):
            self._ui_elements.append(__value)
        super().__setattr__(__name, __value)

    @abstractmethod
    def setup_ui(self, window: QWidget, c: Communicator) -> None:
        """Build user interface"""

    # TODO reuse elements instead of add/remove every time
    def remove_ui(self) -> None:
        """Remove all UI elements from window and clear '_ui_elements' list"""
        for element in self._ui_elements:
            element.deleteLater()
        self._ui_elements = list()


class MainMenuUI(UIBuilder):
    def setup_ui(self, window: QWidget, c: Communicator) -> None:
        def signal_btn_play_menu():
            c.btn_clicked.emit("state:play_menu")

        self.ui_label = QLabel("Game of life")
        self.ui_label.setFont(QFont("Arial", 36))
        self.ui_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.ui_btn_play_menu = QPushButton("Play")
        self.ui_btn_exit = QPushButton("Exit")

        self.ui_btn_play_menu.clicked.connect(signal_btn_play_menu)
        self.ui_btn_exit.clicked.connect(window.close)

        self.ui_layout = QVBoxLayout()
        self.ui_layout.addWidget(self.ui_label)

        self.ui_btnuttons_wrapper = QWidget()

        buttons_layout = QVBoxLayout()
        buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        buttons_layout.addWidget(self.ui_btn_play_menu)
        buttons_layout.addWidget(self.ui_btn_exit)

        self.ui_btnuttons_wrapper.setLayout(buttons_layout)

        self.ui_layout.addWidget(self.ui_btnuttons_wrapper)
        window.layout.addLayout(self.ui_layout, 0, 0)


class PlayMenuUI(UIBuilder):
    def setup_ui(self, window: QWidget, c: Communicator) -> None:
        def signal_btn_play_random():
            c.btn_clicked.emit("state:play_random")

        def signal_btn_map_editor():
            c.btn_clicked.emit("state:map_editor")

        def signal_btn_load_from_file():
            c.btn_clicked.emit("state:load_from_file")

        def signal_btn_go_back():
            c.btn_clicked.emit("state:main_menu")

        self.ui_label = QLabel("Play")
        self.ui_label.setFont(QFont("Arial", 36))
        self.ui_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.ui_btn_play_random = QPushButton("Random alive cells")
        self.ui_btn_map_editor = QPushButton("Map Editor")
        self.ui_btn_load_from_file = QPushButton("Load map from file")
        self.ui_btn_back = QPushButton("Back")

        self.ui_btn_play_random.clicked.connect(signal_btn_play_random)
        self.ui_btn_map_editor.clicked.connect(signal_btn_map_editor)
        self.ui_btn_load_from_file.clicked.connect(signal_btn_load_from_file)
        self.ui_btn_back.clicked.connect(signal_btn_go_back)

        self.ui_layout = QVBoxLayout()
        self.ui_layout.addWidget(self.ui_label)

        self.ui_btnuttons_wrapper = QWidget()

        buttons_layout = QVBoxLayout()
        buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        buttons_layout.addWidget(self.ui_btn_play_random)
        buttons_layout.addWidget(self.ui_btn_map_editor)
        buttons_layout.addWidget(self.ui_btn_load_from_file)
        buttons_layout.addWidget(self.ui_btn_back)

        self.ui_btnuttons_wrapper.setLayout(buttons_layout)

        self.ui_layout.addWidget(self.ui_btnuttons_wrapper)
        window.layout.addLayout(self.ui_layout, 0, 0)


class PlayUI(UIBuilder):
    def setup_ui(self, window: QWidget, c: Communicator) -> None:
        self.ui_layout = QVBoxLayout()
        window.layout.addLayout(self.ui_layout, 0, 0)


class MapEditorUI(UIBuilder):
    def setup_ui(self, window: QWidget, c: Communicator) -> None:
        self.ui_layout = QVBoxLayout()
        window.layout.addLayout(self.ui_layout, 0, 0)


class PauseUI(UIBuilder):
    def setup_ui(self, window: QWidget, c: Communicator) -> None:
        def signal_btn_resume():
            c.btn_clicked.emit("state:play")

        def signal_btn_edit_map():
            c.btn_clicked.emit("state:map_editor")

        def signal_btn_load_from_file():
            c.btn_clicked.emit("command:load_from_file")

        def signal_btn_go_main_menu():
            c.btn_clicked.emit("state:main_menu")

        self.ui_label = QLabel("Pause")
        self.ui_label.setFont(QFont("Arial", 36))
        self.ui_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.ui_btn_resume = QPushButton("Resume")
        self.ui_btn_edit_map = QPushButton("Edit map")
        self.ui_btn_load_from_file = QPushButton("Load from file")
        self.ui_btn_main_menu = QPushButton("Go to main menu")
        self.ui_btn_exit = QPushButton("Exit")

        self.ui_btn_resume.clicked.connect(signal_btn_resume)
        self.ui_btn_edit_map.clicked.connect(signal_btn_edit_map)
        self.ui_btn_load_from_file.clicked.connect(signal_btn_load_from_file)
        self.ui_btn_main_menu.clicked.connect(signal_btn_go_main_menu)
        self.ui_btn_exit.clicked.connect(window.close)

        self.ui_layout = QVBoxLayout()
        self.ui_layout.addWidget(self.ui_label)

        self.ui_btnuttons_wrapper = QWidget()

        buttons_layout = QVBoxLayout()
        buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        buttons_layout.addWidget(self.ui_btn_resume)
        buttons_layout.addWidget(self.ui_btn_edit_map)
        buttons_layout.addWidget(self.ui_btn_load_from_file)
        buttons_layout.addWidget(self.ui_btn_main_menu)
        buttons_layout.addWidget(self.ui_btn_exit)

        self.ui_btnuttons_wrapper.setLayout(buttons_layout)

        self.ui_layout.addWidget(self.ui_btnuttons_wrapper)
        window.layout.addLayout(self.ui_layout, 0, 0)
