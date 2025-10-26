# player.py

import pygame
import math
from gun import Gun
from weapons import PISTOL, SHOTGUN, RIFLE

class Player:
    def __init__(self, x, y, texture):
        self.pos = pygame.math.Vector2(x, y)
        self.width = 28
        self.height = 28
        self.original_image = pygame.transform.scale(texture, (self.width, self.height))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x, y))
        self.hitbox = pygame.Rect(0, 0, self.width * 0.8, self.height * 0.8)
        self.hitbox.center = self.pos
        self.angle = 0
        self.rotation_speed = 3
        self.move_speed = 3
        self.backward_move_speed = 1.5
        self.is_shooting = False
        self.gun = Gun(name="Pistol",
                        cooldown = 200,
                        bullet_speed = 8,
                        bullet_lifetime = 1000,
                        bullet_size = (4, 10),
                        bullet_color = (255,255,0))
        self.health = 100
        self.team = 'police'

        self.weapons = [PISTOL, SHOTGUN, RIFLE]
        self.current_weapon_index = 0
        self.gun = self.weapons[self.current_weapon_index]

        self.is_shooting = False

    def is_dead(self):
        return self.health <= 0

    def shoot(self):
        return self.gun.shoot(self.pos.x, self.pos.y, self.angle, self)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_SHIFT]:
            self.is_shooting = True
        else:
            self.is_shooting = False

        if keys[pygame.K_1]:
            self.current_weapon_index = 0
            self.gun = self.weapons[self.current_weapon_index]
            print(f"Switched to {self.gun.name}")
        if keys[pygame.K_2]:
            self.current_weapon_index = 1
            self.gun = self.weapons[self.current_weapon_index]
            print(f"Switched to {self.gun.name}")
        if keys[pygame.K_3]:
            self.current_weapon_index = 2
            self.gun = self.weapons[self.current_weapon_index]
            print(f"Switched to {self.gun.name}")

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