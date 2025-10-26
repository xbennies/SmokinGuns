import pygame
import sys
from player import Player
from camera import Camera
from map import MAP_LAYOUT, TILE_SIZE, MAP_WIDTH, MAP_HEIGHT
from ai_character import AICharacter
from weapons import PISTOL, SHOTGUN, RIFLE

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Smokin' Guns")
clock = pygame.time.Clock()
FPS = 60

BACKGROUND_COLOR = (30, 30, 30)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
FONT = pygame.font.SysFont('Arial', 50)
BUTTON_FONT = pygame.font.SysFont('Arial', 30)

try:
    wall_texture = pygame.image.load("assets/wall.png").convert()
    floor_texture = pygame.image.load("assets/floor.png").convert()
    police_texture = pygame.image.load("assets/police.png").convert_alpha()
    criminal_texture = pygame.image.load("assets/criminal.png").convert_alpha()
    wall_texture = pygame.transform.scale(wall_texture, (TILE_SIZE, TILE_SIZE))
    floor_texture = pygame.transform.scale(floor_texture, (TILE_SIZE, TILE_SIZE))
except pygame.error as e:
    print(f"Error loading textures: {e}")
    sys.exit()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    global game_state
    
    play_button = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 25, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 50, 200, 50)

    while game_state == 'main_menu':
        screen.fill(BACKGROUND_COLOR)
        
        draw_text('Main Menu', FONT, WHITE, screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
        
        mx, my = pygame.mouse.get_pos()

        # Draw and check buttons
        pygame.draw.rect(screen, GREY, play_button)
        draw_text('Play Game', BUTTON_FONT, WHITE, screen, play_button.centerx, play_button.centery)
        
        pygame.draw.rect(screen, GREY, quit_button)
        draw_text('Quit', BUTTON_FONT, WHITE, screen, quit_button.centerx, quit_button.centery)

        if play_button.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                game_state = 'playing'
        if quit_button.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.quit()
                sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()
        clock.tick(FPS)

def game_loop():
    global game_state

    walls, floor_tiles = [], []
    police_team, criminals_team = [], []
    
    for row_index, row in enumerate(MAP_LAYOUT):
        for col_index, tile_char in enumerate(row):
            x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
            floor_tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile_char == '#': walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif tile_char == 'P':
                player = Player(x + TILE_SIZE / 2, y + TILE_SIZE / 2, police_texture)
                police_team.append(player)
            elif tile_char == 'T': police_team.append(AICharacter(x + TILE_SIZE / 2, y + TILE_SIZE / 2, 'police', police_texture))
            elif tile_char == 'E': criminals_team.append(AICharacter(x + TILE_SIZE / 2, y + TILE_SIZE / 2, 'criminals', criminal_texture))

    camera = Camera(MAP_WIDTH, MAP_HEIGHT)
    bullets = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    game_state = 'main_menu'

        if not running: break

        all_entities = police_team + criminals_team
        player.update(walls)
        for character in all_entities:
            if isinstance(character, AICharacter):
                fired_bullets = character.update(all_entities, walls)
                if fired_bullets: bullets.extend(fired_bullets)
        camera.update(player)
        if player.is_shooting:
            new_bullet = player.shoot()
            if new_bullet: bullets.append(new_bullet)

        for bullet in bullets:
            bullet.update()
            if any(bullet.rect.colliderect(wall) for wall in walls):
                bullet.lifetime = 0
        
        for i in range(len(bullets) - 1, -1, -1):
            bullet = bullets[i]
            hit = False
            for entity in all_entities:
                if bullet.rect.colliderect(entity.hitbox) and bullet.owner.team != entity.team:
                    entity.health -= 25
                    bullets.pop(i)
                    hit = True
                    break
            if hit: continue
        
        bullets = [b for b in bullets if not b.is_dead()]
        police_team = [p for p in police_team if not p.is_dead()]
        criminals_team = [c for c in criminals_team if not c.is_dead()]

        if player not in police_team:
            print("Player eliminated! Returning to menu.")
            running = False
            game_state = 'main_menu'

        screen.fill(BACKGROUND_COLOR)
        for tile in floor_tiles: screen.blit(floor_texture, camera.apply(tile))
        for wall in walls: screen.blit(wall_texture, camera.apply(wall))
        for entity in all_entities: screen.blit(entity.image, camera.apply(entity.rect))
        for bullet in bullets: screen.blit(bullet.image, camera.apply(bullet.rect))
        pygame.display.flip()
        clock.tick(FPS)

game_state = 'main_menu'

while True:
    if game_state == 'main_menu':
        main_menu()
    elif game_state == 'playing':
        game_loop()