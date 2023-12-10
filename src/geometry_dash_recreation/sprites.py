from typing import Any
import pygame
from pygame.sprite import AbstractGroup
from geometry_dash_recreation.constants import *

pygame.init()

# Spieler-Sprites
class Cube(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.original_image = pygame.image.load("assets/textures/icons/cubes/icon_2.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (UNIT, UNIT))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = PLAYER_POS
        self.hitbox = self.image.get_rect()
        self.hitbox.left, self.hitbox.bottom = PLAYER_POS

        self.vel = 0
        self.angle = 0
    
    def jump(self, gravity) -> None:
        self.vel = -JUMP_VEL * gravity
    
    def death_touch(self, sprite: pygame.sprite.Sprite) -> bool:
        return self.hitbox.bottom - DEATH_ACCURACY >= sprite.hitbox.top

    def controls(self, ev, click, gravity, ground: pygame.sprite.Sprite, level_gr: pygame.sprite.Group) -> int:
        # Springen
        if ev:
            if self.hitbox.bottom == ground.rect.top:
                self.jump(gravity)
            for sprite in level_gr:
                if self.hitbox.colliderect(sprite.hitbox.move(0, -1)):
                    self.jump(gravity)
        
        # Einwirkung der Gravitation
        self.hitbox.y += self.vel * DELTA_TIME * RESIZE
        self.vel += VEL_ADD * gravity * DELTA_TIME

        self.angle -= 7

        # Landen auf dem Boden
        if self.hitbox.colliderect(ground.rect.move(0, -1)) and gravity == 1:
            self.angle = round(self.angle / 90) * 90
            self.hitbox.bottom = ground.rect.top
            self.vel = 0
        
        # Landen auf Level-Komponenten
        for sprite in level_gr:
            if sprite.type == "platform":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -1)) and gravity == 1:
                    if self.death_touch(sprite):
                        return 1
                    self.angle = round(self.angle / 90) * 90
                    self.hitbox.bottom = sprite.hitbox.top
                    self.vel = 0
            elif sprite.type == "hazard":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -1)):
                    return 1
        
        self.angle = 0 if self.angle == 360 else self.angle

        return 0
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.hitbox.center)
        return super().update(*args, **kwargs) 

# Background-Sprites
class Ground(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/textures/bg/ground.jpg").convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, GROUND_HEIGHT

class Background(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load("assets/textures/bg/background.png").convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_HEIGHT*2*(16/9), SCREEN_HEIGHT*2))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, -SCREEN_HEIGHT/4
    
    def reset(self):
        self.rect.left, self.rect.top = 0, -SCREEN_HEIGHT/4

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.x -= BACKGROUND_SCROLL_SPEED    # Bewegen des Hintergrunds nach links
        return super().update(*args, **kwargs)

# Component-Sprite (für die Hindernisse im Spiel)
class Component(pygame.sprite.Sprite):
    def __init__(self, imgfile="assets/textures/transparent.png",
                 pos=[0, 0], size=[1, 1], hb_mul=1.0, type="deco", color="yellow", 
                 *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(imgfile).convert_alpha()
        self.image = pygame.transform.scale(self.image, (UNIT*size[0], UNIT*size[1]))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0]*UNIT, pos[1]*UNIT  # Position des Komponenten
        self.hitbox = self.image.get_rect()
        self.hitbox.x, self.hitbox.y = pos[0]*UNIT, pos[1]*UNIT
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
        self.hitbox.center = self.rect.center
        return super().update(*args, **kwargs)
