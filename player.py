# player.py

import pygame
import math
from bullet import Bullet

class Player:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.width = 40
        self.height = 30
        
        self.original_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, (0, 160, 255), (0, 0, self.width, self.height))
        pygame.draw.line(self.original_image, (255, 255, 255), (self.width / 2, self.height / 2), (self.width / 2, 0), 3)
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x, y))

        self.hitbox = pygame.Rect(0, 0, self.width, self.height)
        self.hitbox.center = self.pos

        self.angle = 0
        self.rotation_speed = 3
        self.move_speed = 3
        self.backward_move_speed = 1.5
        self.shoot_cooldown = 200
        self.last_shot_time = 0
        self.is_shooting = False

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_cooldown:
            self.last_shot_time = current_time
            return Bullet(self.pos.x, self.pos.y, self.angle)
        return None

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed
        
        if keys[pygame.K_SPACE]:
            self.is_shooting = True
        else:
            self.is_shooting = False

    def update(self, walls):
        self.handle_input()

        rads = math.radians(self.angle)
        vel_x = 0
        vel_y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            vel_x -= math.sin(rads) * self.move_speed
            vel_y -= math.cos(rads) * self.move_speed
        if keys[pygame.K_DOWN]:
            vel_x += math.sin(rads) * self.backward_move_speed
            vel_y += math.cos(rads) * self.backward_move_speed

        self.pos.x += vel_x
        self.hitbox.centerx = round(self.pos.x)

        for wall in walls:
            if self.hitbox.colliderect(wall):
                if vel_x > 0:
                    self.hitbox.right = wall.left
                if vel_x < 0:
                    self.hitbox.left = wall.right
                self.pos.x = self.hitbox.centerx

        self.pos.y += vel_y
        self.hitbox.centery = round(self.pos.y)

        for wall in walls:
            if self.hitbox.colliderect(wall):
                if vel_y > 0:
                    self.hitbox.bottom = wall.top
                if vel_y < 0:
                    self.hitbox.top = wall.bottom
                self.pos.y = self.hitbox.centery

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)