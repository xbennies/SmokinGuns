import pygame
from bullet import Bullet

class Gun:
    def __init__(self, name, cooldown, bullet_speed, bullet_lifetime, bullet_size, bullet_color):
        self.name = name
        self.cooldown = cooldown
        self.bullet_speed = bullet_speed
        self.bullet_lifetime = bullet_lifetime
        self.bullet_size = bullet_size
        self.bullet_color = bullet_color

        self.last_shot_time = 0

    def shoot(self, x, y, angle):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.cooldown:
            self.last_shot_time = current_time

            return Bullet(x, y, angle,
                        self.bullet_speed,
                        self.bullet_lifetime,
                        self.bullet_size,
                        self.bullet_color)
        return None