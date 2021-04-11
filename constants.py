import math
from game import Color

# ---Constants---
# -Colors-
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
BLUE = Color(66, 135, 245)
# -Game-
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_BACKGROUND = BLUE
CELL_WIDTH = 8
CELL_HEIGHT = 8
CELL_DEFAULT_COLOR = BLUE
N_CELLS_HORIZONTAL = math.ceil(SCREEN_WIDTH / CELL_WIDTH)
N_CELLS_VERTICAL = math.ceil(SCREEN_HEIGHT / CELL_HEIGHT)
N_CELLS = N_CELLS_HORIZONTAL*N_CELLS_VERTICAL
# -----------------
cells = {row: [] for row in range(N_CELLS_HORIZONTAL)}
alive_cells = 0
