import pygame
import sys
from player import Player
from camera import Camera
from bullet import Bullet

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR =(30,30,30)
GRID_COLOR = (60,60,60)
GRID_SQUARE_SIZE = 50
FPS = 60
MAP_WIDTH = 2000
MAP_HEIGHT = 1500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Smokin' Guns")
clock = pygame.time.Clock()

player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
camera = Camera(MAP_WIDTH, MAP_HEIGHT)
bullets = []
walls = [
    pygame.Rect(400, 300, 200, 50),
    pygame.Rect(700, 500, 50, 400),
    pygame.Rect(1000, 200, 400, 50)
]

def draw_grid(surface):
    for x in range(0, MAP_WIDTH, GRID_SQUARE_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, MAP_HEIGHT))
    for y in range(0, MAP_HEIGHT, GRID_SQUARE_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (MAP_WIDTH, y))

map_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
map_surface.fill(BACKGROUND_COLOR)
draw_grid(map_surface)
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