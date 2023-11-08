import pygame
from pygame.sprite import AbstractGroup
from geometry_dash_recreation.constants import *

pygame.init()

class Cube(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load('assets/textures/icons/cubes/icon_1.png')
        self.image = pygame.transform.scale(self.image, (UNIT, UNIT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = PLAYER_POS
        self.hitbox = self.rect
    
    def update(self):
        self.rect.x, self.rect.y = self.hitbox.x, self.hitbox.y
