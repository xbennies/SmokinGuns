import pygame

pygame.init()

TILE_SIZE = 50

wall_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
wall_image.fill((50, 50, 50))
for x in range(0, TILE_SIZE, 10):
    for y in range(0, TILE_SIZE, 10):
        if (x // 10 + y // 10) % 2 == 0:
            pygame.draw.rect(wall_image, (70, 70, 70), (x, y, 10, 10))
pygame.image.save(wall_image, "assets/wall.png")

floor_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
floor_image.fill((120,120,120))
pygame.draw.rect(floor_image, (130, 130, 130), (TILE_SIZE/2 - 2, TILE_SIZE/2 - 2, 4, 4))
pygame.image.save(floor_image, "assets/floor.png")

pygame.quit()
print("Assets generated successfully in the 'assets' folder!")