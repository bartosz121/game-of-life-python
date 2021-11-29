from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Sequence, Iterable
from itertools import chain
from random import randint

from PyQt6.QtWidgets import QWidget
from cell import Cell
from gui.ui import Communicator, UIBuilder, MainMenuUI, PlayMenuUI, PlayUI, PauseUI


class PlayMode:
    """Contains methods needed in 'Play' states"""

    def apply_rules(self, cells: Sequence[Cell]):
        """
        Any live cell with two or three live neighbours survives.
        Any dead cell with three live neighbours becomes a live cell.
        All other live cells die in the next generation.
        All other dead cells stay dead.
        """
        for cell in chain(*cells):
            if cell.is_alive:
                if cell.alive_neighbours != 2 and cell.alive_neighbours != 3:
                    cell.is_alive = False
            else:
                if cell.alive_neighbours == 3:
                    cell.is_alive = True

    def count_neighbours(self, cells):
        y_len, x_len = cells.shape

        for y in range(y_len):
            for x in range(x_len):
                result = 0
                cell = cells[y][x]
                # print(f"{x=} {y=} {str(cell)=}")
                # North
                if y - 1 >= 0:
                    if cells[y - 1][x].is_alive:
                        result += 1
                # South
                if y + 1 <= y_len - 1:
                    if cells[y + 1][x].is_alive:
                        result += 1
                # West
                if x - 1 >= 0:
                    if cells[y][x - 1].is_alive:
                        result += 1
                # East
                if x + 1 <= x_len - 1:
                    if cells[y][x + 1].is_alive:
                        result += 1
                # North-East
                if y - 1 >= 0 and x + 1 <= x_len - 1:
                    if cells[y - 1][x + 1].is_alive:
                        result += 1
                # North-West
                if y - 1 >= 0 and x - 1 >= 0:
                    if cells[y - 1][x - 1].is_alive:
                        result += 1
                # South-East
                if y + 1 <= y_len - 1 and x + 1 <= x_len - 1:
                    if cells[y + 1][x + 1].is_alive:
                        result += 1
                # South-West
                if y + 1 <= y_len - 1 and x - 1 >= 0:
                    if cells[y + 1][x - 1].is_alive:
                        result += 1

                cell.alive_neighbours = result


class GameState(ABC):
    name: str
    allowed: Sequence[str] = []
    ui: UIBuilder

    def switch(self, new_state: GameState, window: QWidget, c: Communicator):
        if new_state.name in self.allowed:
            self.ui.remove_ui()
            self.__class__ = new_state
            self.ui.setup_ui(window, c)
        else:
            msg = "Switching state from {!r} to {!r} not allowed"
            raise ValueError(msg.format(self.name, new_state.name))

    def __repr__(self):
        return f"{type(self).__name__}()"

    def __str__(self):
        return self.name

    @abstractmethod
    def run(self):
        pass


class MainMenu(GameState):
    name = "main_menu"
    allowed = ("play_menu", "settings")
    ui = MainMenuUI()

    def run(self):
        print("main menu state")


class Settings(GameState):
    name = "settings"
    allowed = "main_menu"
    # ui = SettingsUI()

    def run(self):
        print("settings state")


class Pause(GameState):
    name = "pause"
    allowed = ("play", "map_editor", "main_menu")
    ui = PauseUI()

    def run(self):
        print("pause state")


class PlayMenu(GameState):
    name = "play_menu"
    allowed = ("play_random", "map_editor", "main_menu")
    ui = PlayMenuUI()

    def run(self):
        print("play_menu state")


class PlayRandom(GameState, PlayMode):
    name = "play_random"
    allowed = ("map_editor", "pause")
    ui = PlayUI()

    def run(self, cells):
        self.randomize(cells)
        self.randomized = True
        self.__class__ = Play

    def randomize(self, cells):
        """Set given amount of random picked cells isAlive to True"""
        for cell in chain(*cells):
            cell.is_alive = bool(randint(0, 1))


class Play(GameState, PlayMode):
    name = "play"
    allowed = ("map_editor", "pause")
    ui = PlayUI()

    def run(self, cells):
        self.count_neighbours(cells)
        self.apply_rules(cells)
