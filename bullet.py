import pygame
import math

class Bullet:
    def __init__(self, x, y, angle, speed, lifetime, size, color):
        self.pos = pygame.math.Vector2(x, y)
        self.angle = angle
        self.speed = speed

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(color)

        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center = self.pos)

        self.lifetime = lifetime
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        rads = math.radians(self.angle)
        self.pos.x -= math.sin(rads) * self.speed
        self.pos.y -= math.cos(rads) * self.speed
        self.rect.center = self.pos

    def is_dead(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime