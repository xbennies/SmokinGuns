import pygame

class Camera:
    def __init__(self, map_width, map_height):
        self.camera_rect = pygame.Rect(0, 0, map_width, map_height)
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, target_rect):
        return target_rect.move(self.camera_rect.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(pygame.display.get_surface().get_width() / 2)
        y = -target.rect.centery + int(pygame.display.get_surface().get_height() / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.map_width - pygame.display.get_surface().get_width()), x)
        y = max(-(self.map_height - pygame.display.get_surface().get_height()), y)

        self.camera_rect = pygame.Rect(x, y, self.map_width, self.map_height)