import random
import pygame
import time
from cell import Cell
from constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_BACKGROUND, N_CELLS_VERTICAL,\
    N_CELLS_HORIZONTAL, N_CELLS, CELL_WIDTH, CELL_HEIGHT, CELL_DEFAULT_COLOR, BASIC_COLORS


def get_game_info():
    print(f"==============GAME=OF=LIFE===============\n"
          f"SCREEN:\n"
          f"\t{SCREEN_WIDTH}x{SCREEN_HEIGHT}\n"
          f"FPS CAP:\n"
          f"\t{FPS}\n"
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
                if cells[x][y-1].is_alive:
                    result += 1
            # South
            if y+1 <= N_CELLS_VERTICAL-1:
                if cells[x][y+1].is_alive:
                    result += 1
            # West
            if x-1 >= 0:
                if cells[x-1][y].is_alive:
                    result += 1
            # East
            if x+1 <= N_CELLS_HORIZONTAL-1:
                if cells[x+1][y].is_alive:
                    result += 1
            # North-East
            if y-1 >= 0 and x+1 <= N_CELLS_HORIZONTAL-1:
                if cells[x+1][y-1].is_alive:
                    result += 1
            # North-West
            if y-1 >= 0 and x-1 >= 0:
                if cells[x-1][y-1].is_alive:
                    result += 1
            # South-East
            if y+1 <= N_CELLS_VERTICAL-1 and x+1 <= N_CELLS_HORIZONTAL-1:
                if cells[x+1][y+1].is_alive:
                    result += 1
            # South-West
            if y+1 <= N_CELLS_VERTICAL-1 and x-1 >= 0:
                if cells[x-1][y+1].is_alive:
                    result += 1

            cell.num_neighbors = result


def game():
    pygame.init()
    get_game_info()
    pygame.display.set_caption("Conway's Game of Life")
    display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
    display_surface.fill(SCREEN_BACKGROUND.RGB)

    def update_fps():
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, True, BASIC_COLORS["WHITE"].RGB)
        return fps_text

    # Create cells
    for x in range(N_CELLS_HORIZONTAL):
        for y in range(N_CELLS_VERTICAL):
            cells[x].append(Cell(x*CELL_WIDTH, y*CELL_HEIGHT))

    # Set Alive random cells
    for i in range((N_CELLS//100)*95):
        cells[random.randint(0, N_CELLS_HORIZONTAL-1)][random.randint(0, N_CELLS_VERTICAL-1)].is_alive = True
    

    # The R-pentomino
    # cells[81][45].is_alive = True
    # cells[80][47].is_alive = True
    # cells[80][46].is_alive = True
    # cells[79][46].is_alive = True
    # cells[80][45].is_alive = True
    

    # Acorn
    # cells[77][46].is_alive = True
    # cells[78][46].is_alive = True
    # cells[78][44].is_alive = True
    # cells[80][45].is_alive = True
    # cells[81][46].is_alive = True
    # cells[82][46].is_alive = True
    # cells[83][46].is_alive = True

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
                if cell.is_alive:
                    if cell.num_neighbors != 2 and cell.num_neighbors != 3:
                        cell.is_alive = False
                else:
                    if cell.num_neighbors == 3:
                        cell.is_alive = True
                pygame.draw.rect(display_surface, cell.color, cell.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display_surface.blit(update_fps(), (10, 0))
        pygame.display.update()
        clock.tick(FPS)
        # print(pygame.mouse.get_pos())


if __name__ == '__main__':
    cells = {row: [] for row in range(N_CELLS_HORIZONTAL)}
    alive_cells = 0
    game()
