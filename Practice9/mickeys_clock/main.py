import pygame
from clock import MickeyClock

pygame.init()

screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Mickey Clock")

clock_obj = MickeyClock((200, 200))

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock_obj.draw(screen)

    pygame.display.flip()
    clock.tick(1)  # обновление раз в секунду

pygame.quit()
