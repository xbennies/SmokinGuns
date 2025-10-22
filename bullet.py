import pygame
import math

class Bullet:
    def __init__(self, x, y, angle):
        self.pos = pygame.math.Vector2(x, y)
        self.angle = angle
        self.speed = 8

        self.image = pygame.Surface((10, 4), pygame.SRCALPHA)
        self.image.fill((255, 255, 0))

        self.image = pygame.transform.rotate(self.image, self.angle)

        self.rect = self.image.get_rect(center = self.pos)

        self.lifetime = 1000
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        rads = math.radians(self.angle)
        self.pos.x -= math.sin(rads) * self.speed
        self.pos.y -= math.cos(rads) * self.speed

        self.rect.center = self.pos

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

    def kill(self):
        pass