from typing import Any
import pygame
from pygame.sprite import AbstractGroup
from geometry_dash_recreation.constants import *

pygame.init()

# Spieler-Sprites
class Cube(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load("assets/textures/icons/cubes/icon_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (UNIT, UNIT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = PLAYER_POS
        self.hitbox = self.rect

        self.vel = 0
    
    def controls(self, ev, click, gravity, ground, level_gr) -> int:
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
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.x, self.rect.y = self.hitbox.x, self.hitbox.y
        return super().update(*args, **kwargs) 

# Background-Sprites
class Ground(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/textures/bg/ground.jpg").convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, SCREEN_HEIGHT-GROUND_HEIGHT

class Background(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load("assets/textures/bg/background.png").convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH*2, SCREEN_HEIGHT*2))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, -SCREEN_HEIGHT/4

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.x -= DELTA_TIME    # Bewegen des Hintergrunds nach links
        return super().update(*args, **kwargs)

# Component-Sprite (für die Hindernisse im Spiel)
class Component(pygame.sprite.Sprite):
    def __init__(self, imgfile="assets/textures/transparent.png",
                 pos=[0, 0], size=[1, 1], hb_mul=1, type="deco", color="yellow", 
                 *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(imgfile).convert_alpha()
        self.image = pygame.transform.scale(self.image, (UNIT*size[0], UNIT*size[1]))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0]*UNIT, pos[1]*UNIT  # Position des Komponenten
        self.hitbox = self.rect
        self.hitbox.width, self.hitbox.height = \
            self.rect.width*hb_mul, self.rect.height*hb_mul
        # Der Hitbox kann um einen bestimmten Faktor vergrößert oder verkleinert werden

        self.type = type    # platform: Man kann darauf landen und davon abspringen
                            # hazard: Man stirbt, wenn man es berührt
                            # deco: Es zählt als Dekoration und wird vom Spieler ignioriert
                            # ring: Rings, von denen man abspringen kann, wenn man die Maustaste drückt
                            # gravportal: Portale, die die Gravitationsrichtung wechseln
                            # formportal: Portale, die den Spielmodus wechseln

        self.color = color  # Wird als Indentifikation für Rings und Portale verwendet.
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.x -= LEVEL_SCROLL_SPEED
        self.hitbox.x -= LEVEL_SCROLL_SPEED
        return super().update(*args, **kwargs)
