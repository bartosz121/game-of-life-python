import random
import pygame
from cell import Cell
from settings import FONT_SIZE, UI_SCALE, N_CELLS_VERTICAL, N_CELLS_HORIZONTAL,\
    SCREEN_BACKGROUND, BASIC_COLORS, CELL_WIDTH, CELL_HEIGHT, N_CELLS, CELL_DEFAULT_COLOR


class Foo:
    def __init__(self, seed_val):
        self.value = seed_val # call the setter

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Game:
    def __init__(self, s_width, s_height, fps):
        pygame.init()
        pygame.display.set_caption("Conway's Game of Life")
        self.running = True
        self.playing = False
        self.mode = self.main_menu
        self.game_state = "main_menu"
        self.screen_width = s_width
        self.screen_height = s_height
        self.fps = fps
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.START_GAME_KEY, self.PAUSE_KEY, self.QUIT_KEY = False, False, False
        self.fonts = {
            "small": pygame.font.SysFont("Arial", FONT_SIZE["SMALL"]),
            "standard": pygame.font.SysFont("Arial", FONT_SIZE["NORMAL"]),
            "medium": pygame.font.SysFont("Arial", FONT_SIZE["MEDIUM"]),
            "big": pygame.font.SysFont("Arial", FONT_SIZE["BIG"])
        }

        # Buttons prefix:
        # mm_ = main_menu
        # sg_ = start_game
        # p_ = paused
        # s_ = settings
        self.buttons = {}
        self.cells = {row: [] for row in range(N_CELLS_HORIZONTAL)}
        self.alive_cells = 0

        self.get_game_info()
        self.display.fill(SCREEN_BACKGROUND.RGB)

    @property
    def screen_width(self):
        return self._screen_width

    @screen_width.setter
    def screen_width(self, value):
        if value < 600:
            raise ValueError("Window resolution must be >= 600x400")
        self._screen_width = value

    @property
    def screen_height(self):
        return self._screen_height

    @screen_height.setter
    def screen_height(self, value):
        if value < 400:
            raise ValueError("Window resolution must be >= 600x400")
        self._screen_height = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        if value == "main_menu":
            self._game_state = value
            self.mode = self.main_menu
        elif value == "start_game_menu":
            self._game_state = value
            self.mode = self.start_game_menu
        elif value == "playing":
            self._game_state = value
            self.mode = self.play
        elif value == "map_editor":
            self._game_state = value
            self.mode = self.map_editor
        elif value == "settings":
            self._game_state = value
            self.mode = self.settings_menu
        elif value == "paused":
            self._game_state = value
            self.mode = self.pause
        else:
            self.game_state = "main_menu"

    @property
    def START_GAME_KEY(self):
        return self.START_GAME_KEY

    @START_GAME_KEY.setter
    def START_GAME_KEY(self, value):
        if value:
            self.game_state = "playing"

    @property
    def PAUSE_KEY(self):
        return self.PAUSE_KEY

    @PAUSE_KEY.setter
    def PAUSE_KEY(self, value):
        if value:
            if self.game_state == "playing":
                self.game_state = "paused"
            elif self.game_state == "paused":
                self.game_state = "playing"

    @property
    def QUIT_KEY(self):
        return self.QUIT_KEY

    @QUIT_KEY.setter
    def QUIT_KEY(self, value):
        if value:
            pygame.quit()

    def _get_fps(self):
        return str(int(self.clock.get_fps()))

    def game_loop(self):
        while self.running:
            self.check_events()
            if self.game_state == "playing":
                self.clock.tick(self.fps)
            else:
                self.clock.tick(60)
            self.reset_keys()
            self.run_state()
            self.draw_text(self._get_fps(), self.fonts["standard"],
            BASIC_COLORS["WHITE"].RGB, (10, 0), center=False)
            pygame.display.update()

            # print(pygame.mouse.get_pos())

    def run_state(self):
        return self.mode()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.PAUSE_KEY = True
                if event.key == pygame.K_q:
                    self.QUIT_KEY = True
                if event.key == pygame.K_s and self.game_state == "map_editor":
                    self.START_GAME_KEY = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.check_mouse_click()

    def check_mouse_click(self):
        mx, my = pygame.mouse.get_pos()
        if self.game_state == "main_menu":
            if self.buttons["mm_start_game"].collidepoint((mx, my)):
                self.game_state = "start_game_menu"
            elif self.buttons["mm_settings"].collidepoint((mx, my)):
                self.game_state = "settings"
            elif self.buttons["mm_quit"].collidepoint((mx, my)):
                pygame.quit()
        elif self.game_state == "start_game_menu":
            if self.buttons["sg_random"].collidepoint((mx, my)):
                self.create_clean_game_state(mode="random")
                self.game_state = "playing"
            elif self.buttons["sg_map_editor"].collidepoint((mx, my)):
                self.create_cells()
                self.game_state = "map_editor"
            elif self.buttons["sg_back"].collidepoint((mx, my)):
                self.game_state = "main_menu"
        elif self.game_state == "paused":
            if self.buttons["p_save_current"].collidepoint((mx, my)):
                self.game_state = "main_menu"
            # TODO make a way to save starting state
            # TODO check if map editor current state works properly(setting the self.cells)
            elif self.buttons["p_edit_current"].collidepoint((mx, my)):
                self.game_state = "map_editor"
            elif self.buttons["p_save_start"].collidepoint((mx, my)):
                self.game_state = "main_menu"
            elif self.buttons["p_edit_start"].collidepoint((mx, my)):
                self.game_state = "map_editor"
            elif self.buttons["p_main_menu"].collidepoint((mx, my)):
                self.game_state = "main_menu"
        elif self.game_state == "settings":
            # TODO settings
            if self.buttons["s_todo1"].collidepoint((mx, my)):
                self.game_state = "main_menu"
            elif self.buttons["s_todo2"].collidepoint((mx, my)):
                self.game_state = "main_menu"
            elif self.buttons["s_back"].collidepoint((mx, my)):
                self.game_state = "main_menu"
        elif self.game_state == "map_editor":
            for x in range(N_CELLS_HORIZONTAL):
                for y in range(N_CELLS_VERTICAL):
                    cell = self.cells[x][y]
                    if cell.rect.collidepoint((mx, my)):
                        # 'not cell.is_alive' => logical negation
                        # (True -> False // False -> True)
                        cell.is_alive = not cell.is_alive

    # Game modes
    def main_menu(self):
        self.display.fill(SCREEN_BACKGROUND.RGB)
        self.draw_text("Game of Life", self.fonts["medium"], BASIC_COLORS["BLACK"].RGB,
                       (self.screen_width // 2, self.screen_height // 2 - (self.screen_height // 100 * 30)))

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 - (self.screen_height // 100 * 10)),
                                   (140*UI_SCALE, 30*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "mm_start_game",
                                   "Start game", self.fonts["standard"], BASIC_COLORS["BLACK"].RGB)

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 + (self.screen_height // 100 * 10)),
                                   (140*UI_SCALE, 30*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "mm_settings",
                                   "Settings", self.fonts["standard"], BASIC_COLORS["BLACK"].RGB)

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 + (self.screen_height // 100 * 30)),
                                   (140*UI_SCALE, 30*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "mm_quit",
                                   "Quit", self.fonts["standard"], BASIC_COLORS["BLACK"].RGB)

    def start_game_menu(self):
        self.display.fill(SCREEN_BACKGROUND.RGB)
        self.draw_text("Start Game", self.fonts["medium"], BASIC_COLORS["BLACK"].RGB,
                       (self.screen_width // 2, self.screen_height // 2 - (self.screen_height // 100 * 30)))

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 - (self.screen_height // 100 * 10)),
                                   (140*UI_SCALE, 30*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "sg_random",
                                   "Random alive cells", self.fonts["standard"], BASIC_COLORS["BLACK"].RGB)

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 + (self.screen_height // 100 * 10)),
                                   (140*UI_SCALE, 30*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "sg_map_editor",
                                   "Map editor", self.fonts["standard"], BASIC_COLORS["BLACK"].RGB)

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 + (self.screen_height // 100 * 30)),
                                   (140*UI_SCALE, 30*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "sg_back",
                                   "Go back", self.fonts["standard"], BASIC_COLORS["BLACK"].RGB)

    def settings_menu(self):
        self.display.fill(SCREEN_BACKGROUND.RGB)
        self.draw_text("Settings", self.fonts["medium"], BASIC_COLORS["BLACK"].RGB,
                       (self.screen_width // 2, self.screen_height // 2 - (self.screen_height // 100 * 30)))

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 - (self.screen_height // 100 * 10)),
                                   (140*UI_SCALE, 30*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "s_todo1",
                                   "TODO", self.fonts["standard"], BASIC_COLORS["BLACK"].RGB)

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 + (self.screen_height // 100 * 10)),
                                   (140*UI_SCALE, 30*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "s_todo2",
                                   "TODO", self.fonts["standard"], BASIC_COLORS["BLACK"].RGB)

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 + (self.screen_height // 100 * 30)),
                                   (140*UI_SCALE, 30*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "s_back",
                                   "TODO", self.fonts["standard"], BASIC_COLORS["BLACK"].RGB)

    def play(self):
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
        self.count_neighbors()

        for x in range(N_CELLS_HORIZONTAL):
            for y in range(N_CELLS_VERTICAL):
                cell = self.cells[x][y]

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
                pygame.draw.rect(self.display, cell.color, cell.rect)

    def map_editor(self):
        self.display.fill(SCREEN_BACKGROUND.RGB)
        # self.check_mouse_click()
        for x in range(N_CELLS_HORIZONTAL):
            for y in range(N_CELLS_VERTICAL):
                cell = self.cells[x][y]
                pygame.draw.rect(self.display, cell.color, cell.rect)

    def pause(self):
        self.draw_text("PAUSED", self.fonts["medium"], BASIC_COLORS["WHITE"].RGB,
                       (self.screen_width // 2, self.screen_height // 2 - (self.screen_height // 100 * 30)))
        self.draw_text("Click p to unpause", self.fonts["small"],
                       BASIC_COLORS["WHITE"].RGB,
                       (self.screen_width // 2, self.screen_height // 2 - (self.screen_height // 100 * 20)))

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 - (self.screen_height // 100 * 12)),
                                   (80*UI_SCALE, 15*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "p_save_current",
                                   "Save current state", self.fonts["small"], BASIC_COLORS["BLACK"].RGB)

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 - (self.screen_height // 100 * 4)),
                                   (80*UI_SCALE, 15*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "p_edit_current",
                                   "Edit current state", self.fonts["small"], BASIC_COLORS["BLACK"].RGB)

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 + (self.screen_height // 100 * 4)),
                                   (80*UI_SCALE, 15*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "p_save_start",
                                   "Save starting state", self.fonts["small"], BASIC_COLORS["BLACK"].RGB)

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 + (self.screen_height // 100 * 12)),
                                   (80*UI_SCALE, 15*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "p_edit_start",
                                   "Edit starting state", self.fonts["small"], BASIC_COLORS["BLACK"].RGB)

        self.draw_button_with_text((self.screen_width // 2, self.screen_height // 2 + (self.screen_height // 100 * 30)),
                                   (80*UI_SCALE, 15*UI_SCALE), BASIC_COLORS["WHITE"].RGB, "p_main_menu",
                                   "Back to Main Menu", self.fonts["small"], BASIC_COLORS["BLACK"].RGB)

    # 'Playing' mode methods
    def count_neighbors(self):
        for x in range(N_CELLS_HORIZONTAL):
            for y in range(N_CELLS_VERTICAL):
                result = 0
                cell = self.cells[x][y]
                # North
                if y - 1 >= 0:
                    if self.cells[x][y - 1].is_alive:
                        result += 1
                # South
                if y + 1 <= N_CELLS_VERTICAL - 1:
                    if self.cells[x][y + 1].is_alive:
                        result += 1
                # West
                if x - 1 >= 0:
                    if self.cells[x - 1][y].is_alive:
                        result += 1
                # East
                if x + 1 <= N_CELLS_HORIZONTAL - 1:
                    if self.cells[x + 1][y].is_alive:
                        result += 1
                # North-East
                if y - 1 >= 0 and x + 1 <= N_CELLS_HORIZONTAL - 1:
                    if self.cells[x + 1][y - 1].is_alive:
                        result += 1
                # North-West
                if y - 1 >= 0 and x - 1 >= 0:
                    if self.cells[x - 1][y - 1].is_alive:
                        result += 1
                # South-East
                if y + 1 <= N_CELLS_VERTICAL - 1 and x + 1 <= N_CELLS_HORIZONTAL - 1:
                    if self.cells[x + 1][y + 1].is_alive:
                        result += 1
                # South-West
                if y + 1 <= N_CELLS_VERTICAL - 1 and x - 1 >= 0:
                    if self.cells[x - 1][y + 1].is_alive:
                        result += 1

                cell.num_neighbors = result

    def create_cells(self):
        for x in range(N_CELLS_HORIZONTAL):
            for y in range(N_CELLS_VERTICAL):
                self.cells[x].append(Cell(x * CELL_WIDTH, y * CELL_HEIGHT))

    def set_alive_random_cells(self):
        for i in range((N_CELLS // 100) * 95):
            self.cells[random.randint(0, N_CELLS_HORIZONTAL - 1)][
                random.randint(0, N_CELLS_VERTICAL - 1)].is_alive = True

    def create_clean_game_state(self, mode):
        self.create_cells()
        if mode == "random":
            self.set_alive_random_cells()
        else:
            self.set_alive_random_cells()

    # Pygame/Info methods
    def draw_text(self, text, font, color, pos, center=True):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        if center:
            pos = (pos[0] - text_rect.centerx, pos[1] - text_rect.centery)

        text_rect.topleft = pos
        self.display.blit(text_obj, text_rect)

    def draw_button(self, pos, size, color, name):
        btn = pygame.Rect(pos, size)
        self.buttons[name] = btn
        btn.topleft = (pos[0]-size[0]//2, pos[1]-size[1]//2)
        pygame.draw.rect(self.display, color, btn)

    def draw_button_with_text(self, pos, size, btn_color, btn_name, text, font, text_color):
        self.draw_button(pos, size, btn_color, btn_name)
        self.draw_text(text, font, text_color, pos)

    def reset_keys(self):
        self.START_GAME_KEY, self.PAUSE_KEY, self.QUIT_KEY = False, False, False

    def get_game_info(self):
        print(f"==============GAME=OF=LIFE===============\n"
              f"SCREEN:\n"
              f"\t{self.screen_width}x{self.screen_height}\n"
              f"FPS CAP:\n"
              f"\t{self.fps}\n"
              f"CELL:\n"
              f"\tSIZE: {CELL_WIDTH}x{CELL_HEIGHT}\n"
              f"\tCOLOR: {CELL_DEFAULT_COLOR}\n"
              f"\tCELLS PER ROW: {N_CELLS_HORIZONTAL}\n"
              f"\tCELLS PER COL: {N_CELLS_VERTICAL}\n"
              f"\tN: {N_CELLS}\n"
              f"========================================")
