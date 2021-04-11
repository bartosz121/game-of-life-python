import random
import pygame
import time
from constants import *


class Color:
    def __init__(self, r, g ,b):
        self._r = r
        self._g = g
        self._b = b
        self.RGB = (self._r, self._g, self._b)

    def __repr__(self):
        return f"{self.RGB}"


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._color = CELL_DEFAULT_COLOR.RGB
        self._isAlive = False
        self._numNeighbors = 0
        # pygame.Rect(left, top, width, height)
        # pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
        self.rect = pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)

    def __repr__(self):
        return f"============================\n" \
               f"\tCell({self.x}, {self.y})\n" \
               f"\tisAlive: {self.isAlive}\n" \
               f"\tNeighbors(Alive): {self.numNeighbors}\n" \
               f"\tColor: {self.color}\n" \
               f"============================"

    def check_position(self):
        return f"({self.x}, {self.y})"

    @property
    def numNeighbors(self):
        return self._numNeighbors

    @numNeighbors.setter
    def numNeighbors(self, n):
        self._numNeighbors = n

    @property
    def isAlive(self):
        return self._isAlive

    @isAlive.setter
    def isAlive(self, state: bool):
        # if cell is alive change color to black if not to background color
        if state:
            self.color = BLACK
        else:
            self.color = SCREEN_BACKGROUND
        self._isAlive = state

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color: Color):
        self._color = new_color.RGB

##################################################################


def get_game_info():
    print(f"==============GAME=OF=LIFE===============\n"
          f"SCREEN:\n"
          f"\t{SCREEN_WIDTH}x{SCREEN_HEIGHT}\n"
          f"CELL:\n"
          f"\tSIZE: {CELL_WIDTH}x{CELL_HEIGHT}\n"
          f"\tCOLOR: {CELL_DEFAULT_COLOR}\n"
          f"\tCELLS PER ROW: {N_CELLS_HORIZONTAL}\n"
          f"\tCELLS PER COL: {N_CELLS_VERTICAL}\n"
          f"\tN: {N_CELLS}\n"
          f"========================================")


def count_neighbors():
    for x in range(N_CELLS_HORIZONTAL):
        for y in range(N_CELLS_VERTICAL):
            result = 0
            cell = cells[x][y]
            # North
            if y-1 >= 0:
                if cells[x][y-1].isAlive:
                    result += 1
            # South
            if y+1 <= N_CELLS_VERTICAL-1:
                if cells[x][y+1].isAlive:
                    result += 1
            # West
            if x-1 >= 0:
                if cells[x-1][y].isAlive:
                    result += 1
            # East
            if x+1 <= N_CELLS_HORIZONTAL-1:
                if cells[x+1][y].isAlive:
                    result += 1
            # North-East
            if y-1 >= 0 and x+1 <= N_CELLS_HORIZONTAL-1:
                if cells[x+1][y-1].isAlive:
                    result += 1
            # North-West
            if y-1 >= 0 and x-1 >= 0:
                if cells[x-1][y-1].isAlive:
                    result += 1
            # South-East
            if y+1 <= N_CELLS_VERTICAL-1 and x+1 <= N_CELLS_HORIZONTAL-1:
                if cells[x+1][y+1].isAlive:
                    result += 1
            # South-West
            if y+1 <= N_CELLS_VERTICAL-1 and x-1 >= 0:
                if cells[x-1][y+1].isAlive:
                    result += 1

            cell.numNeighbors = result


def game():
    pygame.init()
    get_game_info()
    pygame.display.set_caption("Conway's Game of Life")
    display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    display_surface.fill(SCREEN_BACKGROUND.RGB)

    # Create cells
    for x in range(N_CELLS_HORIZONTAL):
        for y in range(N_CELLS_VERTICAL):
            cells[x].append(Cell(x*CELL_WIDTH, y*CELL_HEIGHT))

    # Set Alive random cells
    for i in range(N_CELLS//2):
        cells[random.randint(0, N_CELLS_HORIZONTAL-1)][random.randint(0, N_CELLS_VERTICAL-1)].isAlive = True

    # Game loop
    while True:
        count_neighbors()
        for x in range(N_CELLS_HORIZONTAL):
            for y in range(N_CELLS_VERTICAL):
                cell = cells[x][y]

                # Check for rules here
                # Any live cell with two or three live neighbours survives.
                # Any dead cell with three live neighbours becomes a live cell.
                # All other live cells die in the next generation.
                # All other dead cells stay dead.
                if cell.isAlive:
                    if cell.numNeighbors != 2 and cell.numNeighbors != 3:
                        cell.isAlive = False
                else:
                    if cell.numNeighbors == 3:
                        cell.isAlive = True
                pygame.draw.rect(display_surface, cell.color, cell.rect)
        # DONT USE SLEEP FIX LATER
        time.sleep(0.01)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # print(pygame.mouse.get_pos())


if __name__ == '__main__':
    game()
