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
