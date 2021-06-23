from game import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, FPS)

if __name__ == '__main__':
    while game.running:
        game.game_loop()
