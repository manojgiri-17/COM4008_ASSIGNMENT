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

# ==========================================
# EXPLOSION
# ==========================================
class Explosion:
    def _init_(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.frames = explosion_frames

        if self.frames:
            self.frame_count = len(self.frames)
            self.duration = self.frame_count * 2
        else:
            self.frame_count = 20
            self.duration = 20

        self.alive = True

    def update(self):
        self.timer += 1
        if self.timer >= self.duration:
            self.alive = False

    def draw(self, surf):
        if self.frames:
            idx = min(self.frame_count - 1, self.timer // 2)
            frame = self.frames[idx]
            surf.blit(frame, frame.get_rect(center=(self.x, self.y)))
        else:
            t = self.timer / self.duration
            radius = int(5 + 40 * t)
            alpha = max(0, 255 - int(255 * t))
            tmp = pygame.Surface((radius*2+4, radius*2+4), pygame.SRCALPHA)
            pygame.draw.circle(tmp, (255,170,0,alpha),
                               (radius+2,radius+2), radius)
            surf.blit(tmp, (self.x-radius-2, self.y-radius-2))

# ==========================================
# INVADER SETUP
# ==========================================
rows_setup = [
    (inv1_img, 30),
    (inv2_img, 20),
    (inv3_img, 10),
    (inv3_img, 10),
]

invaders = []

def spawn_invaders(cols=10, start_x=40, start_y=80, sx=48, sy=48):
    invaders.clear()
    for r, (img, pts) in enumerate(rows_setup):
        y = start_y + r * sy
        for c in range(cols):
            x = start_x + c * sx
            invaders.append(Invader(x, y, img, pts))

spawn_invaders()

# ==========================================
# GAME STATE
# ==========================================
player = Player(WIDTH//2 - Player.WIDTH//2, HEIGHT - 90)
player_bullets = []
enemy_bullets = []
explosions = []

barriers = [
    Barrier(60, HEIGHT - 200),
    Barrier(180, HEIGHT - 200),
    Barrier(300, HEIGHT - 200),
    Barrier(420, HEIGHT - 200),
]

score = 0
lives = 3
level = 1
highscore = load_highscore()

move_right = True
enemy_speed = 0.5
enemy_drop_speed = 18
enemy_shoot_rate = 2000
last_enemy_shot = pygame.time.get_ticks()

player_shot_cooldown = 250
last_player_shot = 0

# ==========================================
# MUSIC
# ==========================================
if music_loaded:
    try:
        pygame.mixer.music.play(-1)
    except:
        pass

# ==========================================
# HEART DRAW
# ==========================================
def draw_hearts(surf, lives_count, x, y):
    if heart_img:
        w = heart_img.get_width()
        for i in range(lives_count):
            surf.blit(heart_img, (x + i*(w+10), y))
    else:
        for i in range(lives_count):
            pygame.draw.circle(surf, RED, (x+20*i+6, y+10), 6)
            pygame.draw.circle(surf, RED, (x+20*i+18, y+10), 6)
            pygame.draw.polygon(surf, RED,
                [(x+20*i, y+10), (x+20*i+24, y+10), (x+20*i+12, y+26)]
            )

# ==========================================
# MAIN LOOP
# ==========================================
running = True
game_over = False

while running:
    dt = clock.tick(FPS)

    # Background
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(BG_COLOR)

    # Stars
    for star in stars:
        star.update()
        star.draw(screen)

    # ---------------------------
    # EVENTS
    # ---------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                score = 0
                lives = 3
                level = 1
                enemy_speed = 0.5
                enemy_shoot_rate = 2000
                spawn_invaders()
                player.x = WIDTH//2 - Player.WIDTH//2
                player_bullets.clear()
                enemy_bullets.clear()
                explosions.clear()
                barriers = [
                    Barrier(60, HEIGHT - 200),
                    Barrier(180, HEIGHT - 200),
                    Barrier(300, HEIGHT - 200),
                    Barrier(420, HEIGHT - 200),
                ]
                game_over = False
    
    # ---------------------------
    # PLAYER CONTROL
    # ---------------------------
    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT]:
            player.x -= player.speed
        if keys[pygame.K_RIGHT]:
            player.x += player.speed

        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - last_player_shot >= player_shot_cooldown and len(player_bullets) < 5:
                bx = player.x + player.rect.width//2 - 3
                by = player.y
                player_bullets.append(Bullet(bx, by, -10, GREEN))

                explosions.append(Explosion(bx + 3, by + 10))
                last_player_shot = now

                if shoot_sound:
                    try: shoot_sound.play()
                    except: pass

        player.x = max(0, min(player.x, WIDTH - player.rect.width))
        player.update()
    
    # ---------------------------
    # ENEMY MOVEMENT
    # ---------------------------
    move_down = False
    for inv in invaders:
        test_x = inv.x + (enemy_speed if move_right else -enemy_speed)
        if test_x <= 8 or test_x + inv.rect.width >= WIDTH - 8:
            move_down = True
            break

    for inv in invaders:
        inv.x += enemy_speed if move_right else -enemy_speed

    if move_down:
        move_right = not move_right
        for inv in invaders:
            inv.y += enemy_drop_speed

    # Invader reaches player
    for inv in invaders:
        if inv.y + inv.rect.height >= player.y:
            game_over = True
            if score > highscore:
                highscore = score
                save_highscore(highscore)
            break
    
    # ---------------------------
    # ENEMY SHOOTING
    # ---------------------------
    now = pygame.time.get_ticks()
    if now - last_enemy_shot > enemy_shoot_rate and invaders and not game_over:
        shooter = random.choice(invaders)
        ex = shooter.x + shooter.rect.width//2 - 3
        ey = shooter.y + shooter.rect.height
        enemy_bullets.append(Bullet(ex, ey, 6, RED))
        last_enemy_shot = now
    