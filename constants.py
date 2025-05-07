import pygame

pygame.init()

WINDOW_SIZE = (700, 800)

# Colors (Pastel tones)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
PASTEL_BLUE = (173, 216, 230)
PASTEL_BLUE_HOVER = (193, 236, 250)
PASTEL_BLUE_DARK = (120, 160, 210)  # Màu đậm hơn cho lựa chọn được chọn
PASTEL_PINK = (255, 182, 193)
PASTEL_PINK_HOVER = (255, 202, 213)
PASTEL_GREEN = (144, 238, 144)
PASTEL_GREEN_HOVER = (164, 255, 164)
PASTEL_YELLOW = (255, 245, 157)
PASTEL_YELLOW_HOVER = (255, 255, 177)
PASTEL_PURPLE = (221, 160, 221)
PASTEL_PURPLE_HOVER = (241, 180, 241)
PASTEL_ORANGE = (255, 218, 185)
PASTEL_ORANGE_HOVER = (255, 238, 205)

FONT = pygame.font.SysFont("arial", 36, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 20, bold=True)
MOVE_FONT = pygame.font.SysFont("arial", 16, bold=True)

MOVE_SOUND = None

try:
    pygame.mixer.music.load("assets/move.wav")
except FileNotFoundError:
    pygame.mixer.music = None
# COPYRIGHT by Perfect Dragon King (PDK)
