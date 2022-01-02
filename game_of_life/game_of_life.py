from __future__ import annotations
from itertools import chain
import math
import numpy as np
import itertools
from PyQt6 import QtGui
from PyQt6.QtCore import QPoint, Qt

from grid import Grid
from cell import Cell
from file_manager import FileManager
from game import Game
from settings import Settings
from game_states import MainMenu, MapEditor, Pause, Play, PlayMenu, PlayRandom, PlayMode
from gui.ui import Communicator, MainMenuUI


class GameOfLife(Game):
    def __init__(self, width: int, height: int, title: str = "Game of Life", *, timer_interval):
        super().__init__(title, width, height, timer_interval=timer_interval)
        self.settings = self._init_settings(Settings(width, height))
        self.window.setStyleSheet(f'background-color: {self.settings.SCREEN_BACKGROUND.name()}')

        self.grid = Grid(self.settings.N_CELLS_VERTICAL, self.settings.N_CELLS_HORIZONTAL)
        self.state = MainMenu()
        self.file_manager = FileManager(self.window, ('*.cells', '*.rle'))

        self.mouse_pos: QPoint = QPoint(0, 0)

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

        for y in range(self.settings.N_CELLS_VERTICAL):
            for x in range(self.settings.N_CELLS_HORIZONTAL):
                self.grid.objects[y][x] = Cell(x * args[0], y * args[1], *args)


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
            for cell in chain(*self.grid):
                cell.draw(painter)
            if isinstance(self.state, MapEditor):
                if self.state.save_area:
                    painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0, 60)))
                    if len(self.state.save_area) == 1:
                        p1_x, p1_y = self._get_xy_from_point(self.state.save_area[0])
                        painter.drawRect(p1_x, p1_y,self.mouse_pos.x() - p1_x, self.mouse_pos.y() - p1_y)
                    else:
                        # len can only be == 2
                        p1_x, p1_y = self._get_xy_from_point(self.state.save_area[0])
                        p2_x, p2_y = self._get_xy_from_point(self.state.save_area[1])
                        painter.drawRect(p1_x, p1_y, p2_x - p1_x,  p2_y - p1_y)
                        self._handle_command('save_to_file')


                elif self.state.loaded_grid:
                    painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                    r_width = self.state.loaded_grid.x * self.settings.CELL_WIDTH
                    r_height = self.state.loaded_grid.y * self.settings.CELL_HEIGHT
                    painter.drawRect(self.mouse_pos.x(), self.mouse_pos.y(), r_width, r_height)
        self.window.update()

    def mouse_move_event(self, event: QtGui.QMouseEvent):
        self.mouse_pos = event.pos()

        if isinstance(self.state, MapEditor):
            if self.state.mouse_btn_pressed:
                btn_type = self.state.mouse_btn_type
                x = self.mouse_pos.x()
                y = self.mouse_pos.y()
                cell = self.grid[y//self.settings.CELL_HEIGHT][x//self.settings.CELL_WIDTH]

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

            if self.state.save_mode:
                if len(self.state.save_area) < 2:
                    match self.state.mouse_btn_type:
                        case Qt.MouseButton.LeftButton:
                            self.state.save_area.append(event.pos())
                        case _:
                            # Exit save mode if any other mouse button is pressed
                            self.state.save_mode = False
                            self.state.save_area.clear()
                            self._handle_state_change("pause")

            elif self.state.loaded_grid:
                match self.state.mouse_btn_type:
                # transpose loaded grid with RMB
                # anti-transpose with MMB
                # place loaded grid with any other button
                    case Qt.MouseButton.RightButton:
                        self.state.loaded_grid.transpose()
                    case Qt.MouseButton.MiddleButton:
                        self.state.loaded_grid.anti_transpose()
                    case _:
                        for y in range(self.state.loaded_grid.y):
                            for x in range(self.state.loaded_grid.x):
                                grid_y = self.mouse_pos.y() // self.settings.CELL_HEIGHT + y
                                grid_x = self.mouse_pos.x() // self.settings.CELL_WIDTH + x

                                try:
                                    self.grid[grid_y][grid_x].is_alive = self.state.loaded_grid[y][x]
                                except IndexError:
                                    # just continue if it doesnt fit inside grid (e.g user placed it at the edge)
                                    continue
                        self.state.loaded_grid = None
            else:
                self.state.mouse_btn_pressed = True
                self.window.mouseMoveEvent(event) # change state of pressed cell, otherwise it would only work 'on move'

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
                    if isinstance(self.state, MapEditor):
                        self.state.save_mode = False
                        self.state.save_area.clear()
                    self._handle_state_change('pause')
                else:
                    self._handle_state_change('main_menu')
            case Qt.Key.Key_M:
                if isinstance(self.state, PlayMode):
                    if self.state.name == 'map_editor':
                        self._handle_state_change('play')
                    else:
                        self._handle_state_change('map_editor')
            case _:
                print(event.key())

    def btn_clicked_handler(self, msg: str) -> None:
        msg_type, msg_content = msg.split(':')

        match msg_type:
            case 'state':
                self._handle_state_change(msg_content)
            case 'command':
                self._handle_command(msg_content)
            case _:
                raise ValueError(f"Unknown btn_clicked msg: {msg!r}")

    def _get_xy_from_point(self, p: QPoint) -> tuple[int, int]:
        """
        Return tuple with x and y from QPoint position

        Returns:
            tuple(x, y)
        """
        x = p.x()
        y = p.y()
        return x, y

    def _get_save_area_data(self) -> Grid:
        x1, y1 = self._get_xy_from_point(self.state.save_area[0])
        x2, y2 = self._get_xy_from_point(self.state.save_area[1])

        # Calculate area 'greedly'
        min_x_grid = math.floor(min(x1, x2) / self.settings.CELL_WIDTH)
        min_y_grid = math.floor(min(y1, y2) / self.settings.CELL_HEIGHT)
        width = math.ceil(abs(x1-x2)  / self.settings.CELL_WIDTH)
        height = math.ceil(abs(y1-y2) / self.settings.CELL_HEIGHT)

        if width == 0 or height == 0:
            raise ValueError(f"({width!r}x{height!r}) Selected area must be greater than 0")

        max_x_grid = min_x_grid + width
        max_y_grid = min_y_grid + height

        selected_cells = self.grid[min_y_grid:max_y_grid, min_x_grid:max_x_grid] # slice 2d array

        selected = Grid(height, width)

        for y,x in itertools.product(range(height), range(width)):
            selected[y][x] = selected_cells[y][x].is_alive

        return selected

    def _handle_state_change(self, msg: str) -> None:
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

    def _handle_command(self, msg: str) -> None:
        match msg:
            case 'select_save_area':
                self._handle_state_change('map_editor')
                self.state.save_mode = True
            case 'save_to_file':
                save_area_data = self._get_save_area_data()
                self.file_manager.save_file(save_area_data)
                self.state.save_mode = False
                self.state.save_area.clear()
            case 'load_from_file':
                file_grid = self.file_manager.load_file()
                if file_grid:
                    self.state.loaded_grid = file_grid
                self._handle_state_change('map_editor')
            case _:
                raise ValueError(f"Unknown command msg: {msg!r}")

    # Game of Life methods
    def run(self):
        """Responsible for running the game"""
        if isinstance(self.state, PlayMode):
            self.state.run(self.grid.objects)
        else:
            self.state.run()
