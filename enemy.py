import pygame
import math

class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.width = 40
        self.height = 30

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((255,50,50))
        self.rect = self.image.get_rect(center=self.pos)

        self.hitbox = pygame.Rect(0, 0, self.width, self.height)
        self.hitbox.center = self.pos
        
        self.move_speed = 2
        self.vision_radius = 250

        self.health = 100

    def update(self, player, walls):
        player_vector = player.pos - self.pos
        distance = player_vector.length()

        vel_x, vel_y = 0,0

        if distance < self.vision_radius and distance > 0:
            direction_vector = player_vector.normalize()
            vel_x = direction_vector.x * self.move_speed
            vel_y = direction_vector.y * self.move_speed

        self.pos.x += vel_x
        self.hitbox.centerx = round(self.pos.x)
        for wall in walls:
            if self.hitbox.colliderect(wall):
                if vel_x > 0: self.hitbox.right = wall.left
                if vel_x < 0: self.hitbox.left = wall.right
                self.pos.x = self.hitbox.centerx

        self.pos.y += vel_y
        self.hitbox.centery = round(self.pos.y)
        for wall in walls:
            if self.hitbox.colliderect(wall):
                if vel_y > 0: self.hitbox.bottom = wall.top
                if vel_y < 0: self.hitbox.top = wall.bottom
                self.pos.y = self.hitbox.centery

        self.rect.center = self.hitbox.center

    def is_dead(self):
        return self.health <= 0