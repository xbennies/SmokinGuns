import pygame
import sys
from player import Player
from camera import Camera
from bullet import Bullet
from map import MAP_LAYOUT, TILE_SIZE

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR =(30,30,30)
GRID_COLOR = (60,60,60)
FPS = 60

from map import MAP_WIDTH, MAP_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Smokin' Guns")
clock = pygame.time.Clock()

walls = []
for row_index, row in enumerate(MAP_LAYOUT):
    for col_index, tile in enumerate(row):
        if tile == '#':
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

player = Player(TILE_SIZE * 5, TILE_SIZE * 5)
camera = Camera(MAP_WIDTH, MAP_HEIGHT)
bullets = []

map_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
map_surface.fill(BACKGROUND_COLOR)
map_rect = map_surface.get_rect()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    player.update(walls)
    camera.update(player)

    if player.is_shooting:
        new_bullet = player.shoot()
        if new_bullet:
            bullets.append(new_bullet)

    for bullet in bullets:
        bullet.update()
        for wall in walls:
            if bullet.rect.colliderect(wall):
                bullet.spawn_time = pygame.time.get_ticks() - bullet.lifetime - 1
                break

    bullets = [bullet for bullet in bullets if pygame.time.get_ticks() - bullet.spawn_time <= bullet.lifetime]

    screen.fill(BACKGROUND_COLOR)
    screen.blit(map_surface, camera.apply(map_rect))
    for wall in walls:
        pygame.draw.rect(screen, (150, 150, 150), camera.apply(wall))
    screen.blit(player.image, camera.apply(player.rect))

    for bullet in bullets:
        screen.blit(bullet.image, camera.apply(bullet.rect))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()