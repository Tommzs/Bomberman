import pygame
#Colors
COLOR_BACKGROUND = (153, 153, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

#Menu config
MENU_FPS = 60.0
MENU_BACKGROUND_COLOR = (102, 102, 153)
MENU_TITLE_COLOR = (51, 51, 255)

#Window config
WINDOW_SIZE_PERC = 0.9
TILES_NUM = 13
pygame.display.init()
INFO = pygame.display.Info()
min_size = min(INFO.current_h, INFO.current_w)
WINDOW_SIDE_SIZE = int(min_size * WINDOW_SIZE_PERC)
WINDOW_SIZE = (WINDOW_SIDE_SIZE, WINDOW_SIDE_SIZE)
TILE_SIZE = int(WINDOW_SIDE_SIZE / TILES_NUM)

# Game config
GAME_SPEED = 15
GAME_SPEED_AI_ONLY = 60
GAME_BACKGROUND = (107, 142, 35)

BOMB_TIME = 3000 #ms

FONT_TYPE = 'Bebas'
FONT_SIZE = 30
TEXT_LOSE = 'GAME OVER'
TEXT_WIN = 'WIN'
GRID = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]