import pygame


constrain = lambda val, minVal, maxVal: min(maxVal, max(minVal, val))

WIDTH = 1536
HEIGHT = 864

# Path
draw_path = True

# Colors
MAIN_BG_COLOR = pygame.Color('#222222')
BODY_COLOR = pygame.Color('red')
PATH_COLOR = pygame.Color('green')
INITIAL_VEL_COLOR = pygame.Color('blue')
