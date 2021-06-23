from game import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, INGAME_FPS

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, INGAME_FPS)

if __name__ == '__main__':
    while game.running:
        game.game_loop()
