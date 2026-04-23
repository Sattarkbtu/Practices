import pygame
import sys
import random

pygame.init()

# Screen settings
CELL = 20
WIDTH = 600
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 50, 50)
BLUE = (50, 100, 220)
GRAY = (220, 220, 220)

# Fonts
font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 50)

clock = pygame.time.Clock()

# Snake initial data
snake = [(100, 100), (80, 100), (60, 100)]
dx = CELL
dy = 0

# Food initial position
food = (300, 300)

# Game variables
score = 0
level = 1
speed = 8

# Example walls inside field
walls = []
for x in range(200, 400, CELL):
    walls.append((x, 200))
for x in range(100, 300, CELL):
    walls.append((x, 400))


def draw_grid():
    """Draw light grid for the playing field."""
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(SCREEN, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(SCREEN, GRAY, (0, y), (WIDTH, y))


def draw_snake():
    """Draw snake head and body."""
    for i, block in enumerate(snake):
        color = DARK_GREEN if i == 0 else GREEN
        pygame.draw.rect(SCREEN, color, (block[0], block[1], CELL, CELL))
        pygame.draw.rect(SCREEN, BLACK, (block[0], block[1], CELL, CELL), 1)


def draw_food():
    """Draw food."""
    pygame.draw.rect(SCREEN, RED, (food[0], food[1], CELL, CELL))
    pygame.draw.rect(SCREEN, BLACK, (food[0], food[1], CELL, CELL), 1)


def draw_walls():
    """Draw walls."""
    for wall in walls:
        pygame.draw.rect(SCREEN, BLUE, (wall[0], wall[1], CELL, CELL))
        pygame.draw.rect(SCREEN, BLACK, (wall[0], wall[1], CELL, CELL), 1)


def generate_food():
    """
    Generate food in a random valid cell.
    Food must not appear:
    - on a wall
    - on the snake
    """
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        pos = (x, y)
        if pos not in walls and pos not in snake:
            return pos


def game_over_screen():
    """Display game over message."""
    SCREEN.fill(WHITE)
    text1 = big_font.render("Game Over", True, RED)
    text2 = font.render(f"Score: {score}", True, BLACK)
    text3 = font.render(f"Level: {level}", True, BLACK)

    SCREEN.blit(text1, (WIDTH // 2 - text1.get_width() // 2, 220))
    SCREEN.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 300))
    SCREEN.blit(text3, (WIDTH // 2 - text3.get_width() // 2, 330))
    pygame.display.update()
    pygame.time.delay(2000)


running = True
while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Change direction with arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx = 0
                dy = -CELL
            elif event.key == pygame.K_DOWN and dy == 0:
                dx = 0
                dy = CELL
            elif event.key == pygame.K_LEFT and dx == 0:
                dx = -CELL
                dy = 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx = CELL
                dy = 0

    # Move snake
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)

    # Check border collision / leaving playing area
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        game_over_screen()
        pygame.quit()
        sys.exit()

    # Check wall collision
    if new_head in walls:
        game_over_screen()
        pygame.quit()
        sys.exit()

    # Check self collision
    if new_head in snake:
        game_over_screen()
        pygame.quit()
        sys.exit()

    snake.insert(0, new_head)

    # Check food collision
    if new_head == food:
        score += 1
        food = generate_food()

        # Level up every 4 points
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    # Drawing
    SCREEN.fill(WHITE)
    draw_grid()
    draw_walls()
    draw_snake()
    draw_food()

    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)

    SCREEN.blit(score_text, (10, 10))
    SCREEN.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

    pygame.display.update()
