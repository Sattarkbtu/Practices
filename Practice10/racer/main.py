import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()

# Game settings
FPS = 60
FramePerSec = pygame.time.Clock()
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)
GRAY = (120, 120, 120)

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer")

# Fonts similar to tutorial ending
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Simple background replacement
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(GREEN)

# Road surface
road = pygame.Surface((260, SCREEN_HEIGHT))
road.fill(GRAY)

# Dashed road line animation
line_y = 0


def draw_road():
    """Draw the road similar to a racing game background."""
    global line_y

    DISPLAYSURF.blit(background, (0, 0))
    DISPLAYSURF.blit(road, (70, 0))

    # Road borders
    pygame.draw.line(DISPLAYSURF, WHITE, (70, 0), (70, SCREEN_HEIGHT), 5)
    pygame.draw.line(DISPLAYSURF, WHITE, (330, 0), (330, SCREEN_HEIGHT), 5)

    # Middle dashed line
    for y in range(-40, SCREEN_HEIGHT, 80):
        pygame.draw.rect(DISPLAYSURF, WHITE, (195, y + line_y, 10, 40))

    line_y += SPEED
    if line_y >= 80:
        line_y = 0


class Enemy(pygame.sprite.Sprite):
    """
    Enemy sprite.
    This class follows the tutorial style where enemy moves down continuously.
    """

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 90), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, RED, (0, 0, 50, 90), border_radius=8)
        pygame.draw.rect(self.image, BLACK, (0, 0, 50, 90), 2, border_radius=8)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(100, 300), -100)

    def move(self):
        """
        Move enemy downward.
        If enemy leaves the screen, respawn it and increase score.
        """
        global SCORE
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = -100
            self.rect.center = (random.randint(100, 300), -50)


class Player(pygame.sprite.Sprite):
    """
    Player sprite.
    This is kept in the same spirit as the CodersLegacy tutorial:
    player moves only left and right.
    """

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 90), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, BLUE, (0, 0, 50, 90), border_radius=8)
        pygame.draw.rect(self.image, BLACK, (0, 0, 50, 90), 2, border_radius=8)
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)

    def move(self):
        """Move player using left and right arrow keys."""
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 70:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        if self.rect.right < 330:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    """
    Randomly appearing coin on the road.
    This is the extra task added on top of the tutorial.
    """

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (12, 12), 12)
        pygame.draw.circle(self.image, BLACK, (12, 12), 12, 2)
        self.rect = self.image.get_rect()
        self.active = False
        self.hide()

    def hide(self):
        """Hide the coin outside the screen."""
        self.rect.center = (-100, -100)
        self.active = False

    def spawn(self):
        """Spawn coin at random road position."""
        self.rect.center = (random.randint(95, 305), -20)
        self.active = True

    def move(self):
        """Move coin downward when active."""
        if self.active:
            self.rect.move_ip(0, SPEED)
            if self.rect.top > SCREEN_HEIGHT:
                self.hide()


# Create objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Sprite groups like in tutorial part 2
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Tutorial-style custom events
INC_SPEED = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2

pygame.time.set_timer(INC_SPEED, 1000)
pygame.time.set_timer(SPAWN_COIN, 1800)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.2

        if event.type == SPAWN_COIN:
            if not C1.active:
                C1.spawn()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background and road first
    draw_road()

    # Show score and collected coins
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coins_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)

    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - coins_text.get_width() - 10, 10))

    # Update and draw all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)

    P1.move()
    E1.move()
    C1.move()

    # Coin collection
    if C1.active and pygame.sprite.collide_rect(P1, C1):
        COINS_COLLECTED += 1
        C1.hide()

    # Collision with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
