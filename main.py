import pygame
import sys
from player import Player
from camera import Camera
from map import MAP_LAYOUT, TILE_SIZE, MAP_WIDTH, MAP_HEIGHT
from enemy import Enemy

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR =(30,30,30)
GRID_COLOR = (60,60,60)
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Smokin' Guns")
clock = pygame.time.Clock()

try:
    wall_texture = pygame.image.load("assets/wall.png").convert()
    floor_texture = pygame.image.load("assets/floor.png").convert()
except pygame.error as e:
    print(f"Error loading textures: {e}")
    sys.exit()

wall_texture = pygame.transform.scale(wall_texture, (TILE_SIZE, TILE_SIZE))
floor_texture = pygame.transform.scale(floor_texture, (TILE_SIZE, TILE_SIZE))

walls = []
floor_tiles = []
for row_index, row in enumerate(MAP_LAYOUT):
    for col_index, tile in enumerate(row):
        if tile == '#':
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
player_spawn = (0,0)
enemies = []

for row_index, row in enumerate(MAP_LAYOUT):
    for col_index, tile in enumerate(row):
        x = col_index * TILE_SIZE
        y = row_index * TILE_SIZE

        floor_tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

        if tile == '#':
            walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
        if tile == 'P':
            player_spawn = (x + TILE_SIZE / 2, y + TILE_SIZE / 2)
        if tile == 'E':
            enemies.append(Enemy(x + TILE_SIZE / 2, y + TILE_SIZE / 2))

player = Player(player_spawn[0], player_spawn[1])
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

    for enemy in enemies:
        enemy.update(player, walls)

    if player.is_shooting:
        new_bullet = player.shoot()
        if new_bullet:
            bullets.append(new_bullet)

    for bullet in bullets:
        bullet.update()
        hit_wall = False
        for wall in walls:
            if bullet.rect.colliderect(wall):
                hit_wall = True
                break
        if hit_wall:
            bullet.lifetime = 0

    for i in range(len(bullets) - 1, -1, -1):
        bullet = bullets[i]
        for j in range(len(enemies) - 1, -1, -1):
            enemy = enemies[j]
            if bullet.rect.colliderect(enemy.hitbox):
                enemy.health -= 25
                bullets.pop(i)
                break

    bullets = [bullet for bullet in bullets if not bullet.is_dead()]
    enemies = [enemy for enemy in enemies if not enemy.is_dead()]

    screen.fill(BACKGROUND_COLOR)

    for tile_rect in floor_tiles:
        screen.blit(floor_texture, camera.apply(tile_rect))
    for wall_rect in walls:
        screen.blit(wall_texture, camera.apply(wall_rect))

    for enemy in enemies:
        screen.blit(enemy.image, camera.apply(enemy.rect))

    screen.blit(player.image, camera.apply(player.rect))

    for bullet in bullets:
        screen.blit(bullet.image, camera.apply(bullet.rect))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()