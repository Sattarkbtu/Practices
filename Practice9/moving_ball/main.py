import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

ball = Ball(WIDTH // 2, HEIGHT // 2)

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        ball.move(-ball.speed, 0, WIDTH, HEIGHT)
    if keys[pygame.K_RIGHT]:
        ball.move(ball.speed, 0, WIDTH, HEIGHT)
    if keys[pygame.K_UP]:
        ball.move(0, -ball.speed, WIDTH, HEIGHT)
    if keys[pygame.K_DOWN]:
        ball.move(0, ball.speed, WIDTH, HEIGHT)

    ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
