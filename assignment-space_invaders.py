import pygame
import random
import sys
import os

# ==========================================
# SETTINGS
# ==========================================
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
FPS = 60

# ==========================================
# ASSET FILENAMES
# ==========================================
SOUND_SHOOT = "shoot.wav"
SOUND_EXPLODE = "explosion.wav"
MUSIC_BG = "bg_music.mp3"
HEART_IMG = "heart.png"
HIGH_SCORE_FILE = "highscore.txt"
BACKGROUND_IMG = "background.png"
EXPLOSION_FRAME_COUNT = 8
GAME_OVER_IMG = "gameover.png"

# ==========================================
# SAFE LOAD FUNCTIONS
# ==========================================
def load_sound(filename):
    try:
        if os.path.exists(filename):
            return pygame.mixer.Sound(filename)
    except:
        pass
    return None

def load_music(filename):
    try:
        if os.path.exists(filename):
            pygame.mixer.music.load(filename)
            return True
    except:
        pass
    return False

def load_image(filename):
    try:
        if os.path.exists(filename):
            return pygame.image.load(filename).convert_alpha()
    except:
        pass
    return None

def load_highscore():
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read().strip() or 0)
    except:
        pass
    return 0

def save_highscore(value):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(int(value)))
    except:
        pass

# ==========================================
# LOAD ASSETS
# ==========================================
shoot_sound = load_sound(SOUND_SHOOT)
explode_sound = load_sound(SOUND_EXPLODE)
music_loaded = load_music(MUSIC_BG)
heart_img = load_image(HEART_IMG)
background_img = load_image(BACKGROUND_IMG)
game_over_img = load_image(GAME_OVER_IMG)

explosion_frames = []
for i in range(EXPLOSION_FRAME_COUNT):
    f = load_image(f"explosion_{i}.png")
    if f:
        explosion_frames.append(f)

inv1_img = load_image("invader1.png")
inv2_img = load_image("invader2.png")
inv3_img = load_image("invader3.png")

# ==========================================
# FONTS & COLORS
# ==========================================
font = pygame.font.SysFont("Arial", 26)
big_font = pygame.font.SysFont("Arial", 44)

WHITE = (255, 255, 255)
RED = (220, 40, 40)
GREEN = (0, 200, 0)
BG_COLOR = (6, 6, 12)

# ==========================================
# STAR CLASS FOR BLINKING STARS
# ==========================================
class Star:
    def _init_(self, x, y):
        self.x = x
        self.y = y
        self.blink_timer = random.randint(0, 120)
        self.blink_interval = random.randint(60, 180)
        self.visible = True

    def update(self):
        self.blink_timer += 1
        if self.blink_timer >= self.blink_interval:
            self.visible = not self.visible
            self.blink_timer = 0
            self.blink_interval = random.randint(60, 180)

    def draw(self, surf):
        if self.visible:
            pygame.draw.circle(surf, WHITE, (self.x, self.y), 1)

# ==========================================
# CREATE STARS
# ==========================================
stars = []
num_stars = 100
for _ in range(num_stars):
    stars.append(Star(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    