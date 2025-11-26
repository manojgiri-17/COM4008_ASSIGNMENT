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

# ==========================================
# BARRIER CLASS
# ==========================================
class Barrier:
    def _init_(self, x, y, width=80, height=40, health=15):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.health = health
        self.max_health = health
        self.rect = pygame.Rect(x, y, width, height)

    def hit(self, damage=1):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        percent = self.health / self.max_health
        self.h = max(0, int(40 * percent))
        self.rect = pygame.Rect(self.x, self.y + (40 - self.h), self.w, self.h)

    def draw(self, surf):
        if self.health > 0:
            pygame.draw.rect(surf, (0, 255, 0), self.rect)

# ==========================================
# PLAYER CLASS
# ==========================================
class Player:
    WIDTH = 100
    HEIGHT = 100
    def _init_(self, x, y):
        img = load_image("defender.png")
        if img:
            self.img = pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
        else:
            self.img = None

        self.x = x
        self.y = y
        self.speed = 6
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

    def update(self):
        self.rect.topleft = (self.x, self.y)

    def draw(self, surf):
        if self.img:
            surf.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(surf, GREEN, self.rect)

# ==========================================
# INVADER CLASS
# ==========================================
class Invader:
    WIDTH = 40
    HEIGHT = 30
    def _init_(self, x, y, image, score):
        if image:
            self.img = pygame.transform.scale(image, (self.WIDTH, self.HEIGHT))
        else:
            self.img = None

        self.x = x
        self.y = y
        self.score = score
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

    def update(self):
        self.rect.topleft = (self.x, self.y)

    def draw(self, surf):
        if self.img:
            surf.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(surf, (180, 80, 200), self.rect)

# ==========================================
# BULLET CLASS
# ==========================================
class Bullet:
    def _init_(self, x, y, vy, color=(0,255,0)):
        self.x = x
        self.y = y
        self.vy = vy
        self.color = color
        self.w = 6
        self.h = 12
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.alive = True

    def update(self):
        self.y += self.vy
        self.rect.topleft = (self.x, self.y)

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
