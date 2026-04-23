import pygame
import random
import sys

pygame.init()

WIDTH = 500
HEIGHT = 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

CLOCK = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)
RED = (220, 50, 50)
BLUE = (50, 100, 220)
GREEN = (50, 200, 100)
ROAD_COLOR = (60, 60, 60)
LINE_COLOR = (240, 240, 240)
BRONZE = (205, 127, 50)
SILVER = (180, 180, 180)
GOLD = (255, 215, 0)

FONT = pygame.font.SysFont("Arial", 28)
BIG_FONT = pygame.font.SysFont("Arial", 48)

ROAD_X = 100
ROAD_WIDTH = 300
LINE_WIDTH = 10
LINE_HEIGHT = 60
line_y = 0


class PlayerCar:
    """Player car."""

    def __init__(self):
        self.width = 50
        self.height = 90
        self.speed = 7
        self.rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 120, self.width, self.height)

    def move(self, keys):
        """Move only left and right inside the road."""
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < ROAD_X:
            self.rect.left = ROAD_X
        if self.rect.right > ROAD_X + ROAD_WIDTH:
            self.rect.right = ROAD_X + ROAD_WIDTH

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=10)


class EnemyCar:
    """Enemy car moving downward."""

    def __init__(self):
        self.width = 50
        self.height = 90
        self.base_speed = random.randint(5, 7)
        self.bonus_speed = 0
        self.reset()

    def reset(self):
        lane_x = random.randint(ROAD_X, ROAD_X + ROAD_WIDTH - self.width)
        self.rect = pygame.Rect(lane_x, random.randint(-700, -100), self.width, self.height)

    @property
    def speed(self):
        return self.base_speed + self.bonus_speed

    def update(self):
        """Move enemy. Return True if it passes the screen."""
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset()
            return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=10)


class Coin:
    """
    Coin with different weights:
    weight 1, 2, 3
    """

    def __init__(self):
        self.radius = 15
        self.rect = pygame.Rect(-100, -100, self.radius * 2, self.radius * 2)
        self.active = False
        self.spawn_timer = 0
        self.weight = 1
        self.color = GOLD

    def spawn(self):
        """Create a new weighted coin on the road."""
        x = random.randint(ROAD_X + 20, ROAD_X + ROAD_WIDTH - 20 - self.radius * 2)
        self.rect = pygame.Rect(x, -30, self.radius * 2, self.radius * 2)
        self.weight = random.choice([1, 2, 3])

        if self.weight == 1:
            self.color = BRONZE
        elif self.weight == 2:
            self.color = SILVER
        else:
            self.color = GOLD

        self.active = True

    def update(self):
        """Spawn coin randomly and move it down."""
        if not self.active:
            self.spawn_timer += 1
            if self.spawn_timer > 30 and random.randint(1, 60) == 1:
                self.spawn()
                self.spawn_timer = 0
        else:
            self.rect.y += 6
            if self.rect.top > HEIGHT:
                self.active = False

    def draw(self, surface):
        """Draw coin if active."""
        if self.active:
            pygame.draw.ellipse(surface, self.color, self.rect)
            pygame.draw.ellipse(surface, BLACK, self.rect, 2)


def draw_road():
    """Draw road and animated center line."""
    SCREEN.fill(GREEN)
    pygame.draw.rect(SCREEN, ROAD_COLOR, (ROAD_X, 0, ROAD_WIDTH, HEIGHT))
    pygame.draw.line(SCREEN, WHITE, (ROAD_X, 0), (ROAD_X, HEIGHT), 5)
    pygame.draw.line(SCREEN, WHITE, (ROAD_X + ROAD_WIDTH, 0), (ROAD_X + ROAD_WIDTH, HEIGHT), 5)

    global line_y
    for y in range(-LINE_HEIGHT, HEIGHT, 100):
        pygame.draw.rect(
            SCREEN,
            LINE_COLOR,
            (WIDTH // 2 - LINE_WIDTH // 2, y + line_y, LINE_WIDTH, LINE_HEIGHT)
        )
    line_y += 8
    if line_y >= 100:
        line_y = 0


def game_over_screen(score, coins):
    """Game over message."""
    SCREEN.fill(BLACK)

    over_text = BIG_FONT.render("GAME OVER", True, RED)
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    coin_text = FONT.render(f"Coins: {coins}", True, GOLD)
    restart_text = FONT.render("Press R to Restart or Q to Quit", True, WHITE)

    SCREEN.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, 220))
    SCREEN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 310))
    SCREEN.blit(coin_text, (WIDTH // 2 - coin_text.get_width() // 2, 350))
    SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 430))
    pygame.display.update()


def run_game():
    """Main racer loop."""
    player = PlayerCar()
    enemies = [EnemyCar(), EnemyCar()]
    coin = Coin()

    score = 0
    collected_coins = 0

    running = True
    game_over = False

    while running:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            keys = pygame.key.get_pressed()
            player.move(keys)

            draw_road()

            for enemy in enemies:
                if enemy.update():
                    score += 1
                enemy.draw(SCREEN)

                if player.rect.colliderect(enemy.rect):
                    game_over = True

            coin.update()
            coin.draw(SCREEN)

            # Collect weighted coin
            if coin.active and player.rect.colliderect(coin.rect):
                collected_coins += coin.weight
                coin.active = False

                # Increase enemy speed when player earns N coins
                if collected_coins % 5 == 0:
                    for enemy in enemies:
                        enemy.bonus_speed += 1

            player.draw(SCREEN)

            score_text = FONT.render(f"Score: {score}", True, WHITE)
            coin_text = FONT.render(f"Coins: {collected_coins}", True, GOLD)
            weight_info = FONT.render(f"Coin value: {coin.weight if coin.active else '-'}", True, WHITE)

            SCREEN.blit(score_text, (20, 20))
            SCREEN.blit(coin_text, (WIDTH - coin_text.get_width() - 20, 20))
            SCREEN.blit(weight_info, (20, 55))

            pygame.display.update()

        else:
            game_over_screen(score, collected_coins)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_r]:
                run_game()
                return
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    run_game()
