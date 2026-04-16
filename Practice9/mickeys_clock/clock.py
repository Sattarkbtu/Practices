import pygame
import datetime
import os

class MickeyClock:
    def __init__(self, center):
        self.center = center

        base = os.path.dirname(__file__)

        # ФОН (экранға сай масштаб)
        self.bg = pygame.image.load(os.path.join(base, "images", "background.png"))
        self.bg = pygame.transform.scale(self.bg, (400, 400))

        # ТІЛДЕР
        self.minute_hand = pygame.image.load(os.path.join(base, "images", "minute.png"))
        self.second_hand = pygame.image.load(os.path.join(base, "images", "second.png"))

    def rotate_hand(self, image, angle, center, offset):
        rotated = pygame.transform.rotate(image, angle)
        rect = rotated.get_rect(center=(center[0], center[1] + offset))
        return rotated, rect

    def draw(self, screen):
        now = datetime.datetime.now()

        sec_angle = -now.second * 6
        min_angle = -now.minute * 6

        # ФОН (ортасына)
        bg_rect = self.bg.get_rect(center=self.center)
        screen.blit(self.bg, bg_rect)

        # МИНУТ ТІЛІ
        min_rot, min_rect = self.rotate_hand(
            self.minute_hand, min_angle, self.center, 20
        )

        # СЕКУНД ТІЛІ
        sec_rot, sec_rect = self.rotate_hand(
            self.second_hand, sec_angle, self.center, 30
        )

        # САЛУ
        screen.blit(min_rot, min_rect)
        screen.blit(sec_rot, sec_rect)
