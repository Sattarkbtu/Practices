import pygame
import random
import sys
import time

pygame.init()

# Window settings
WIDTH = 640
HEIGHT = 640
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Grid settings
CELL_SIZE = 20
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 60, 60)
BLUE = (60, 120, 255)
GOLD = (255, 215, 0)
PURPLE = (160, 60, 220)
GRAY = (80, 80, 80)

# Fonts
FONT = pygame.font.SysFont("Arial", 28)
BIG_FONT = pygame.font.SysFont("Arial", 52)

CLOCK = pygame.time.Clock()

# Border and inside walls
WALLS = set()

for x in range(COLS):
    WALLS.add((x, 0))
    WALLS.add((x, ROWS - 1))

for y in range(ROWS):
    WALLS.add((0, y))
    WALLS.add((COLS - 1, y))

for x in range(10, 22):
    WALLS.add((x, 10))
for x in range(8, 18):
    WALLS.add((x, 20))


class Snake:
    """Snake object with body, direction and growth logic."""

    def __init__(self):
        self.body = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.grow = False

    def change_direction(self, new_dir):
        """Prevent direct reverse movement."""
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def move(self):
        """Move snake one cell."""
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def check_collision(self):
        """Check wall, border and self collision."""
        head = self.body[0]
        x, y = head

        if x < 0 or x >= COLS or y < 0 or y >= ROWS:
            return True

        if head in WALLS:
            return True

        if head in self.body[1:]:
            return True

        return False

    def draw(self, surface):
        """Draw snake head and body."""
        for i, segment in enumerate(self.body):
            rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)


class Food:
    """
    Food with:
    - random weight
    - different color
    - disappearing timer
    """

    def __init__(self, snake_body):
        self.position = None
        self.weight = 1
        self.color = RED
        self.spawn_time = time.time()
        self.lifetime = 6  # seconds
        self.respawn(snake_body)

    def random_position(self, snake_body):
        """Food must not appear on walls or snake."""
        while True:
            pos = (random.randint(1, COLS - 2), random.randint(1, ROWS - 2))
            if pos not in WALLS and pos not in snake_body:
                return pos

    def respawn(self, snake_body):
        """Create a new food with random weight and fresh timer."""
        self.position = self.random_position(snake_body)
        self.weight = random.choice([1, 2, 3])

        # Different colors for different weights
        if self.weight == 1:
            self.color = RED
            self.lifetime = 7
        elif self.weight == 2:
            self.color = GOLD
            self.lifetime = 5
        else:
            self.color = PURPLE
            self.lifetime = 4

        self.spawn_time = time.time()

    def expired(self):
        """Return True if food lifetime is over."""
        return time.time() - self.spawn_time >= self.lifetime

    def draw(self, surface):
        """Draw food."""
        rect = pygame.Rect(self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


def draw_grid():
    """Draw background grid."""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(SCREEN, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(SCREEN, GRAY, (0, y), (WIDTH, y))


def draw_walls():
    """Draw walls."""
    for wall in WALLS:
        rect = pygame.Rect(wall[0] * CELL_SIZE, wall[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(SCREEN, BLUE, rect)
        pygame.draw.rect(SCREEN, BLACK, rect, 1)


def game_over_screen(score, level):
    """Show final result."""
    SCREEN.fill(BLACK)
    text1 = BIG_FONT.render("GAME OVER", True, RED)
    text2 = FONT.render(f"Score: {score}", True, WHITE)
    text3 = FONT.render(f"Level: {level}", True, WHITE)
    text4 = FONT.render("Press R to Restart or Q to Quit", True, WHITE)

    SCREEN.blit(text1, (WIDTH // 2 - text1.get_width() // 2, 220))
    SCREEN.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 310))
    SCREEN.blit(text3, (WIDTH // 2 - text3.get_width() // 2, 350))
    SCREEN.blit(text4, (WIDTH // 2 - text4.get_width() // 2, 420))
    pygame.display.update()


def run_game():
    """Main game loop."""
    snake = Snake()
    food = Food(snake.body)

    score = 0
    level = 1
    speed = 8
    foods_eaten_this_level = 0

    running = True
    game_over = False

    while running:
        CLOCK.tick(speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        if not game_over:
            snake.move()

            if snake.check_collision():
                game_over = True

            # Food disappears after some time
            if food.expired():
                food.respawn(snake.body)

            # Snake eats food
            if snake.body[0] == food.position:
                snake.grow = True
                score += food.weight
                foods_eaten_this_level += 1
                food.respawn(snake.body)

                # Level up every 3 foods eaten
                if foods_eaten_this_level >= 3:
                    level += 1
                    speed += 2
                    foods_eaten_this_level = 0

            SCREEN.fill(WHITE)
            draw_grid()
            draw_walls()
            snake.draw(SCREEN)
            food.draw(SCREEN)

            score_text = FONT.render(f"Score: {score}", True, BLACK)
            level_text = FONT.render(f"Level: {level}", True, BLACK)
            weight_text = FONT.render(f"Food weight: {food.weight}", True, BLACK)

            SCREEN.blit(score_text, (15, 10))
            SCREEN.blit(level_text, (WIDTH - level_text.get_width() - 15, 10))
            SCREEN.blit(weight_text, (15, 45))

            pygame.display.update()

        else:
            game_over_screen(score, level)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_r]:
                run_game()
                return
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    run_game()
