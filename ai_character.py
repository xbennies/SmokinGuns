import pygame
import math
from weapons import PISTOL

class AICharacter:
    def __init__(self, x, y, team):
        self.pos = pygame.math.Vector2(x, y)
        self.width = 40
        self.height = 30

        self.team = team

        self.original_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.team == 'police':
            self.original_image.fill((0, 160, 255))
        else:
            self.original_image.fill((255, 50, 50))

        pygame.draw.line(self.original_image, (255,255,255), (self.width / 2, self.height / 2), (self.width /2, 0), 3)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = pygame.Rect(0, 0, self.width, self.height)
        self.hitbox.center = self.pos
        
        self.move_speed = 2.2
        self.vision_radius = 350
        self.health = 100

        self.gun = PISTOL
        self.angle = 0
        self.shooting_range = 350

    def update(self, all_entities, walls):
        target = None
        closest_dist = float('inf')
        bullets_fired = []

        for entity in all_entities:
            if entity.team != self.team:
                dist = self.pos.distance_to(entity.pos)
                if dist < closest_dist and dist < self.vision_radius:
                    closest_dist = dist
                    target = entity

        vel_x, vel_y = 0, 0
        if target:
            direction_vector = (target.pos - self.pos).normalize()
            vel_x = direction_vector.x * self.move_speed
            vel_y = direction_vector.y * self.move_speed
            self.angle = (target.pos - self.pos).angle_to(pygame.math.Vector2(0, -1))

            if closest_dist < self.shooting_range:
                new_bullet = self.gun.shoot(self.pos.x, self.pos.y, self.angle, self)
                if new_bullet:
                    bullets_fired.append(new_bullet)

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

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.hitbox.center)

        return bullets_fired

    def is_dead(self):
        return self.health <= 0