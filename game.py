import math
import pygame


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
        self.color = CELL_DEFAULT_COLOR.RGB
        self.isAlive = False
        self.numNeighbors = 0
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

    def set_alive(self, state: bool):
        self.isAlive = state

    def set_color(self, new_color: Color):
        self.color = new_color.RGB


# ---Constants---
# -Colors-
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
BLUE = Color(66, 135, 245)
# -Game-
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_BACKGROUND = BLUE
CELL_WIDTH = 16
CELL_HEIGHT = 16
CELL_DEFAULT_COLOR = BLACK
N_CELLS_HORIZONTAL = math.ceil(SCREEN_WIDTH / CELL_WIDTH)
N_CELLS_VERTICAL = math.ceil(SCREEN_HEIGHT / CELL_HEIGHT)


def get_game_info():
    print(f"==============GAME=OF=LIFE===============\n"
          f"SCREEN:\n"
          f"\t{SCREEN_WIDTH}x{SCREEN_HEIGHT}\n"
          f"CELL:\n"
          f"\tSIZE: {CELL_WIDTH}x{CELL_HEIGHT}\n"
          f"\tCOLOR: {CELL_DEFAULT_COLOR}\n"
          f"\tCELLS PER ROW: {N_CELLS_HORIZONTAL}\n"
          f"\tCELLS PER COL: {N_CELLS_VERTICAL}\n"
          f"\tN: {N_CELLS_HORIZONTAL*N_CELLS_VERTICAL}\n"
          f"========================================")


def game():
    pygame.init()
    get_game_info()
    display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create cells
    # pygame.Rect(left, top, width, height)
    # pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)

    # Game loop
    while True:
        display_surface.fill(SCREEN_BACKGROUND.RGB)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # testing
            c1 = Cell(100, 200)
            pygame.draw.rect(display_surface, c1.color, c1)
            pygame.display.flip()
            # print(pygame.mouse.get_pos())
            pygame.display.update()


if __name__ == '__main__':
    game()