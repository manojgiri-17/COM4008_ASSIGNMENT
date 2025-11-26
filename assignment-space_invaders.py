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
