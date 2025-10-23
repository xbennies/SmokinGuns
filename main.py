import pygame
import sys
from player import Player
from camera import Camera
from map import MAP_LAYOUT, TILE_SIZE, MAP_WIDTH, MAP_HEIGHT
from ai_character import AICharacter

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
police_team = []
criminals_team = []

for row_index, row in enumerate(MAP_LAYOUT):
    for col_index, tile_char in enumerate(row):
        x = col_index * TILE_SIZE
        y = row_index * TILE_SIZE

        floor_tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

        if tile_char == '#':
            walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
        elif tile_char == 'P':
            player = Player(x + TILE_SIZE / 2, y + TILE_SIZE / 2)
            police_team.append(player)
        elif tile_char == 'T':
            teammate = AICharacter(x + TILE_SIZE / 2, y + TILE_SIZE / 2, team='police')
            police_team.append(teammate)
        if tile_char == 'E':
            enemy = AICharacter(x + TILE_SIZE / 2, y + TILE_SIZE / 2, team='criminals')
            criminals_team.append(enemy)

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

    all_entities = police_team + criminals_team

    player.update(walls)

    for character in all_entities:
        if isinstance(character, AICharacter):
            fired_bullets = character.update(all_entities, walls)
            if fired_bullets:
                bullets.extend(fired_bullets)

    camera.update(player)

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
        bullet_removed = False
        for entity in all_entities:
            if bullet.rect.colliderect(entity.hitbox) and bullet.owner.team != entity.team:
                entity.health -= 25
                bullets.pop(i)
                bullet_removed = True
                break
        if bullet_removed: continue

    bullets = [bullet for bullet in bullets if not bullet.is_dead()]
    police_team = [member for member in police_team if not member.is_dead()]
    criminals_team = [member for member in criminals_team if not member.is_dead()]

    if player not in police_team:
        print("Player has been eliminated!")
        running = False

    screen.fill(BACKGROUND_COLOR)
    for tile_rect in floor_tiles:
        screen.blit(floor_texture, camera.apply(tile_rect))
    for wall_rect in walls:
        screen.blit(wall_texture, camera.apply(wall_rect))

    for character in all_entities:
        screen.blit(character.image, camera.apply(character.rect))

    for bullet in bullets: screen.blit(bullet.image, camera.apply(bullet.rect))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()