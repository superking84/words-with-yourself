import random

# A list of color presets
WHITE = (255, 255, 255)
TRANSPARENT = (255, 255, 255, 0)
BLACK = (0, 0, 0)
DARK_GREY = (84, 84, 84)
LIGHT_GREY = (168, 168, 168)
SILVER = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 20, 147)
PURPLE = (160, 32, 240)
ALL_COLORS = [WHITE, BLACK, DARK_GREY, SILVER, RED, GREEN, BLUE, YELLOW, ORANGE, PINK, PURPLE]

def get_random_color():
    return tuple([random.randint(0,255) for value in ['r', 'g', 'b']])