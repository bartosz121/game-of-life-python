from __future__ import annotations
from itertools import chain
import math
from PyQt6 import QtCore
import numpy as np
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from numpy.lib.arraysetops import isin

from cell import Cell
from game_refactor import Game
from settings import Settings
from game_states import MainMenu, MapEditor, Pause, Play, PlayMenu, PlayRandom, PlayMode
from gui.ui import Communicator, MainMenuUI


class GameOfLife(Game):
    def __init__(self, width: int, height: int, title: str = "Game of Life", *, timer_interval):
        super().__init__(title, width, height, timer_interval=timer_interval)
        self.settings = self._init_settings(Settings(width, height))
        self.window.setStyleSheet(f'background-color: {self.settings.SCREEN_BACKGROUND.name()}')
        self.state = MainMenu()
        self.c = Communicator()
        self.c.btn_clicked.connect(self.btn_clicked_handler)
        # pyqt event listeners
        self.window.paintEvent = self.paint_event
        self.window.keyPressEvent = self.key_press_event
        self.window.mouseMoveEvent = self.mouse_move_event
        self.window.mouseReleaseEvent = self.mouse_release_event
        self.window.mousePressEvent = self.mouse_press_event

        self.initialize_game()

    def initialize_game(self):
        self._create_cells()
        self.state.ui.setup_ui(self.window, self.c)
        print(self.settings)
        super().initialize_game()

    # Game initialization methods
    def _create_cells(self):
        args = (
            self.settings.CELL_WIDTH,
            self.settings.CELL_HEIGHT,
            self.settings.CELL_ALIVE_COLOR,
            self.settings.CELL_DEAD_COLOR,
        )

        cells_gen = (
            Cell(x * args[0], y * args[1], *args)
            for y in range(self.settings.N_CELLS_VERTICAL)
            for x in range(self.settings.N_CELLS_HORIZONTAL)
        )

        # Create cells array and reshape to 2D (cells[y][x])
        self.cells = np.array([*cells_gen]).reshape(
                self.settings.N_CELLS_VERTICAL,
                self.settings.N_CELLS_HORIZONTAL,
            )

    def _init_settings(self, settings: object) -> object:
        """Initialize game settings using those defined in settings.py;
        updated with those to be calculated;"""
        cells_horizontal = math.ceil(self.window.size().width() / settings.CELL_WIDTH)
        cells_vertical = math.ceil(self.window.size().height() / settings.CELL_HEIGHT)
        n_cells = cells_horizontal * cells_vertical

        settings.N_CELLS_HORIZONTAL = cells_horizontal
        settings.N_CELLS_VERTICAL = cells_vertical
        settings.N_CELLS = n_cells

        return settings

    # PyQt listeners
    def paint_event(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self.window)
        if isinstance(self.state, PlayMode):
            for cell in chain(*self.cells):
                cell.draw(painter)
        self.window.update()

    def mouse_move_event(self, event: QtGui.QMouseEvent):
        if isinstance(self.state, MapEditor):
            if self.state.mouse_btn_pressed:
                pos = event.pos()
                btn_type = self.state.mouse_btn_type
                x = pos.x()
                y = pos.y()
                cell = self.cells[y//self.settings.CELL_HEIGHT][x//self.settings.CELL_WIDTH]

                # left btn draws; right btn erases; any other draws;
                match btn_type:
                    case Qt.MouseButton.LeftButton:
                        cell.is_alive = True
                    case Qt.MouseButton.RightButton:
                        cell.is_alive = False
                    case _:
                        cell.is_alive = True

    def mouse_press_event(self, event: QtGui.QMouseEvent):
        if isinstance(self.state, MapEditor):
            self.state.mouse_btn_type = event.button()
            self.state.mouse_btn_pressed = True
            self.window.mouseMoveEvent(event) # change state of pressed cell; otherwise it would only work 'on move'

    def mouse_release_event(self, event: QtGui.QMouseEvent):
        if isinstance(self.state, MapEditor):
            self.state.mouse_btn_pressed = False

    def key_press_event(self, event: QtGui.QKeyEvent) -> None:
        """
        Keyboard shortcuts

        State:
            Key: Action

        =======================================

        PlayMode:
            ESC: Change state to 'Pause'
            M: Change state to 'Map Editor'

        MapEditor:
            M: Change state to 'Play'
        """
        match event.key():
            case Qt.Key.Key_Escape:
                if isinstance(self.state, PlayMode):
                    self._handle_state_change('state:pause')
                else:
                    self._handle_state_change('state:main_menu')
            case Qt.Key.Key_M:
                if isinstance(self.state, PlayMode):
                    if self.state.name == 'map_editor':
                        self._handle_state_change('state:play')
                    else:
                        self._handle_state_change('state:map_editor')
            case _:
                print(event.key())

    def btn_clicked_handler(self, msg: str) -> None:
        if msg.startswith("state:"):
            self._handle_state_change(msg)
        else:
            raise ValueError(f"Unknown btn_clicked msg: {msg!r}")

    def _handle_state_change(self, msg: str) -> None:
        msg = msg[6:] # 'state:new_state' -> 'new_state'
        match msg:
            case "main_menu":
                self._create_cells() # recreate cells
                new_state = MainMenu
            case "settings":
                new_state = Settings
            case "play_menu":
                new_state = PlayMenu
            case "play_random":
                new_state = PlayRandom
            case "play":
                new_state = Play
            case "pause":
                new_state = Pause
            case "map_editor":
                new_state = MapEditor
            case _:
                new_state = MainMenu
        self.state.switch(new_state, self.window, self.c)

    # Game of Life methods
    def run(self):
        """Responsible for running the game"""
        if isinstance(self.state, PlayMode):
            self.state.run(self.cells)
        else:
            self.state.run()