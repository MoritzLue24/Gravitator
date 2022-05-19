import pygame
from VectorUtils import Vector2


constrain = lambda val, minVal, maxVal: min(maxVal, max(minVal, val))

# Colors
MAIN_BG_COLOR = pygame.Color('#222222')
BODY_COLOR = pygame.Color('red')
PATH_COLOR = pygame.Color('green')
INITIAL_VEL_COLOR = pygame.Color('blue')

# UI
UI_BG = pygame.Color('#181818')
FONT_SIZE = 16
FONT_COLOR = pygame.Color(245, 245, 245)
FONT_PATH = 'Assets/Fonts/Roboto-Regular.ttf'
TEXT_MARGIN = Vector2(3, 3)
PASSIVE_COLOR = pygame.Color(45, 75, 123)
ACTIVE_COLOR = pygame.Color(150, 150, 150)