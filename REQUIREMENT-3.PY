import pygame, random, sys
pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Requirement-3")
clock = pygame.time.Clock()
FPS = 60

WHITE = (255,255,255)
GREEN = (50,220,50)
YELLOW = (240,240,40)
RED = (220,50,50)
BG = (6,6,12)

class Barrier:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 6, 6)
        self.exists = True

    def draw(self, surf):
        if self.exists:
            pygame.draw.rect(surf, GREEN, self.rect)

def create_barrier(x, y):
    BARRIER_MASK = [
        "000111111111000",
        "001111111111100",
        "011111111111110",
        "011111111111110",
        "011111000111110",
        "011110000011110",
        "011100000001110",
        "011000000000110"
    ]

    blocks = []
    for row, line in enumerate(BARRIER_MASK):
        for col, char in enumerate(line):
            if char == "1":
                blocks.append(Barrier(x + col * 8, y + row * 8))
    return blocks

barriers = []
gap = WIDTH // 5
for i in range(4):
    bx = gap * (i+1) - 60
    by = HEIGHT - 200
    barriers.append(create_barrier(bx, by))

player_bullets = []
enemy_bullets = []

running = True
timer = 0

while running:
    dt = clock.tick(FPS)
    timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # movement  
    for b in player_bullets[:]:
        b.update()
        if b.y < -10:
            player_bullets.remove(b)
            continue

        # check barrier collision
        for barrier in barriers:
            for block in barrier:
                if block.exists and b.rect.colliderect(block.rect):
                    block.exists = False
                    player_bullets.remove(b)
                    break
    
    for b in enemy_bullets[:]:
        b.update()
        if b.y > HEIGHT:
            enemy_bullets.remove(b)
            continue

        # collision with barrier
        for barrier in barriers:
            for block in barrier:
                if block.exists and b.rect.colliderect(block.rect):
                    block.exists = False
                    enemy_bullets.remove(b)
                    break

    screen.fill(BG)

    # draw barriers
    for barrier in barriers:
        for block in barrier:
            block.draw(screen)

    pygame.display.flip()