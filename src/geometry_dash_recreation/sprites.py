import pygame
from pygame.sprite import AbstractGroup
from geometry_dash_recreation.constants import *

pygame.init()

# Spieler-Sprites
class Cube(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load('assets/textures/icons/cubes/icon_1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (UNIT, UNIT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = PLAYER_POS
        self.hitbox = self.rect

        self.vel = 0
    
    def controls(self, ev, click, gravity, ground, level_gr):
        # Springen
        if ev:
            if self.hitbox.bottom == ground.rect.top:
                self.vel = -JUMP_VEL * gravity
            for sprite in level_gr:
                pass
        
        # Einwirkung der Gravitation
        self.hitbox.y += self.vel * DELTA_TIME
        self.vel += VEL_ADD * gravity * DELTA_TIME

        # Landen auf dem Boden
        if self.hitbox.colliderect(ground.rect) and gravity == 1:
            while self.hitbox.colliderect(ground.rect):
                self.hitbox.y -= DELTA_TIME * gravity
            self.vel = 0
        
        return 0

    def update(self):
        self.rect.x, self.rect.y = self.hitbox.x, self.hitbox.y

# Background-Sprites
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/textures/bg/ground.jpg').convert()
        image_size = SCREEN_WIDTH, SCREEN_HEIGHT
        self.image = pygame.transform.scale(self.image, image_size)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, SCREEN_HEIGHT-GROUND_HEIGHT

class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/textures/bg/background.png').convert()
        image_size = SCREEN_HEIGHT*4, SCREEN_HEIGHT*2
        self.image = pygame.transform.scale(self.image, image_size)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, -SCREEN_HEIGHT/4

    def update(self):
        self.rect.x -= DELTA_TIME
