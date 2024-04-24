from typing import Any
import pygame
from pygame.sprite import AbstractGroup
from geometry_dash_recreation.constants import *

pygame.init()


class HitboxSprite(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image_filename = ""
        self.original_image = pygame.Surface((0, 0))
        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.type = ""
        self.color = ""
        self.angle = 0
    
    def __str__(self) -> str:
        return f"Type: {self.type}\nColor: {self.color}\nRect: {self.rect}\nHitbox: {self.hitbox}\n"

    def move_sprite(self, x: int, y: int):
        self.rect.x += x
        self.rect.y += y
        self.hitbox.center = self.rect.center

    def set_sprite_position(self, pos: tuple, mode: str= "xy"):
        if mode == "xy":
            self.rect.x, self.rect.y = pos
        elif mode == "lt":
            self.rect.left, self.rect.top = pos
        elif mode == "lb":
            self.rect.left, self.rect.bottom = pos
        else:
            self.rect.left, self.rect.top = pos
        self.hitbox.center = self.rect.center

    def rotate_sprite(self, angle: int):
        old_center = self.rect.center
        self.angle += angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=old_center)


# Spieler-Sprites
class Cube(HitboxSprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.original_image = pygame.image.load(f"{ASSETS_FOLDER}/textures/icons/cubes/icon_1.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (UNIT, UNIT))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.right, self.rect.bottom = PLAYER_X, PLAYER_Y
        self.hitbox = self.image.get_rect()
        self.hitbox.right, self.hitbox.bottom = PLAYER_X, PLAYER_Y

        self.vel = 0
        self.angle = 0
    
    def reset(self) -> None:
        self.angle = 0
        self.vel = 0
        self.hitbox.right, self.hitbox.bottom = 0, PLAYER_Y
    
    def jump(self, mul) -> None:
        self.vel = -JUMP_VEL * mul
    
    def death_touch(self, gravity: int, sprite: pygame.sprite.Sprite) -> bool:
        if gravity == 1:
            return self.hitbox.bottom - DEATH_ACCURACY >= sprite.hitbox.top
        elif gravity == -1:
            return self.hitbox.bottom + DEATH_ACCURACY <= sprite.hitbox.top

    def controls(self, ev, click, gravity, ground: pygame.sprite.Sprite, ceiling: pygame.sprite.Sprite,
                 level_gr: pygame.sprite.Group, level_gr_unconverted: dict) -> int:
        # Springen
        if ev:
            if self.hitbox.bottom == ground.rect.top:
                self.jump(gravity)
            for sprite in level_gr:
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)) and sprite.type == "platform":
                    self.jump(gravity)
        
        if click:
            for sprite in level_gr:
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    if sprite.type == "ring":
                        if sprite.color == "cyan":
                            self.vel = -gravity * JUMP_VEL / 1.5
                            return CHANGE_GRAVITY
                        self.jump(gravity * RING_VEL[sprite.color])
        
        # Einwirkung der Gravitation
        self.hitbox.y += self.vel * DELTA_TIME * RESIZE
        self.vel += VEL_ADD * gravity * DELTA_TIME

        self.angle -= gravity * 7 * DELTA_TIME

        if self.hitbox.y < OUT_OF_BOUNDS:
            return DEATH

        # Landen auf dem Boden
        if self.hitbox.colliderect(ground.rect.move(0, -gravity)):
            if gravity == -1:
                return DEATH
            self.angle = round(self.angle / 90) * 90
            self.hitbox.bottom = ground.rect.top
            self.vel = 0
        
        # Landen auf Level-Komponenten
        for sprite in level_gr:
            if sprite.type == "platform":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    if self.death_touch(gravity, sprite):
                        return DEATH
                    self.angle = round(self.angle / 90) * 90
                    if gravity == 1:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif gravity == -1:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.vel = 0
            elif sprite.type == "hazard":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    return DEATH
            elif sprite.type == "pad":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    self.jump(gravity * PAD_VEL[sprite.color])
            elif sprite.type == "formportal":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    if sprite.color == "magenta":
                        return SHIP_GAMEMODE
                    elif sprite.color == "red":
                        return BALL_GAMEMODE
        
        self.angle = 0 if self.angle == 360 or self.angle == -360 else self.angle

        return NORMAL
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.hitbox.center)
        return super().update(*args, **kwargs) 


class Ship(HitboxSprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.original_image = pygame.image.load(f"{ASSETS_FOLDER}/textures/icons/ships/ship_01.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (UNIT, UNIT))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.right, self.rect.bottom = PLAYER_X, PLAYER_Y
        self.hitbox = self.image.get_rect()
        self.hitbox.right, self.hitbox.bottom = PLAYER_X, PLAYER_Y

        self.vel = 0
        self.angle = 0
        self.upsidedown = False

    def reset(self) -> None:
        self.angle = 0
        self.vel = 0
        self.hitbox.right, self.hitbox.bottom = 0, PLAYER_Y
        if self.upsidedown:
            self.flip()
    
    def flip(self) -> None:
        self.upsidedown = not self.upsidedown
        y = self.rect.y
        x = self.rect.x
        self.original_image = pygame.transform.flip(self.original_image, False, True)
        self.rect = self.original_image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.vel = -self.vel
    
    def jump(self, mul) -> None:
        self.vel = -JUMP_VEL * mul

    def death_touch(self, gravity: int, sprite: pygame.sprite.Sprite) -> bool:
        if gravity == 1:
            return self.hitbox.bottom - DEATH_ACCURACY >= sprite.hitbox.top
        elif gravity == -1:
            return self.hitbox.bottom + DEATH_ACCURACY <= sprite.hitbox.top

    def controls(self, ev, click, gravity, ground: pygame.sprite.Sprite, ceiling: pygame.sprite.Sprite,
                 level_gr: pygame.sprite.Group, level_gr_unconverted: dict) -> int:    
        if click:
            for sprite in level_gr:
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    if sprite.type == "ring":
                        if sprite.color == "cyan":
                            # self.vel = -gravity * JUMP_VEL / 1.5
                            self.flip()
                            return CHANGE_GRAVITY
                        self.jump(gravity * RING_VEL[sprite.color])
        
        # Einwirkung der Gravitation
        self.hitbox.y += self.vel * DELTA_TIME * RESIZE

        # Fliegen
        if ev:
            self.vel -= VEL_ADD * gravity * DELTA_TIME / 2
        else:
            self.vel += VEL_ADD * gravity * DELTA_TIME / 2
        
        self.vel = -20 if self.vel <= -20 else self.vel
        self.vel = 20 if self.vel >= 20 else self.vel

        self.angle = -self.vel * 2

        # Landen auf dem Boden
        if self.hitbox.colliderect(ground.rect.move(0, -gravity)):
            self.angle = 0
            self.hitbox.bottom = ground.rect.top
            if gravity == 1:
                if not ev:
                    self.vel = 0
            else:
                if ev:
                    self.vel = 0
        
        if self.hitbox.colliderect(ceiling.rect.move(0, -gravity)):
            self.angle = 0
            self.hitbox.top = ceiling.rect.bottom
            if gravity == 1:
                if ev:
                    self.vel = 0
            else:
                if not ev:
                    self.vel = 0
        
        # Landen auf Level-Komponenten
        for sprite in level_gr:
            if sprite.type == "platform":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    if self.death_touch(gravity, sprite):
                        return DEATH
                    if not ev:
                        self.vel = 0
            elif sprite.type == "hazard":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    return DEATH
            elif sprite.type == "pad":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    self.jump(gravity * PAD_VEL[sprite.color])
            elif sprite.type == "formportal":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    if sprite.color == "green":
                        return CUBE_GAMEMODE
                    elif sprite.color == "red":
                        return BALL_GAMEMODE

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.hitbox.center)
        return super().update(*args, **kwargs) 


class Ball(HitboxSprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.original_image = pygame.image.load(f"{ASSETS_FOLDER}/textures/icons/balls/ball_1.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (UNIT, UNIT))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.right, self.rect.bottom = PLAYER_X, PLAYER_Y
        self.hitbox = self.image.get_rect()
        self.hitbox.right, self.hitbox.bottom = PLAYER_X, PLAYER_Y

        self.vel = 0
        self.angle = 0

    def reset(self) -> None:
        self.angle = 0
        self.vel = 0
        self.hitbox.right, self.hitbox.bottom = 0, PLAYER_Y
    
    def jump(self, mul) -> None:
        self.vel = -JUMP_VEL * mul * 0.7

    def death_touch(self, gravity: int, sprite: pygame.sprite.Sprite) -> bool:
        if gravity == 1:
            return self.hitbox.bottom - DEATH_ACCURACY >= sprite.hitbox.top
        elif gravity == -1:
            return self.hitbox.bottom + DEATH_ACCURACY <= sprite.hitbox.top
    
    def change_gravity(self, gravity):
        self.vel = VEL_ADD * -gravity * 5
        return CHANGE_GRAVITY

    def controls(self, ev, click, gravity, ground: pygame.sprite.Sprite, ceiling: pygame.sprite.Sprite,
                 level_gr: pygame.sprite.Group, level_gr_unconverted: dict) -> int:    
        if click:
            for sprite in level_gr:
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    if sprite.type == "ring":
                        if sprite.color == "cyan":
                            # self.vel = -gravity * JUMP_VEL / 1.5
                            return self.change_gravity(gravity)
                        self.jump(gravity * RING_VEL[sprite.color])
        
        # Einwirkung der Gravitation
        self.hitbox.y += self.vel * DELTA_TIME * RESIZE

        self.vel += VEL_ADD * gravity * DELTA_TIME / 2
        
        self.vel = -40 if self.vel <= -40 else self.vel
        self.vel = 40 if self.vel >= 40 else self.vel

        self.angle -= VEL_ADD * gravity * 4 * DELTA_TIME

        # Landen auf dem Boden
        if self.hitbox.colliderect(ground.rect.move(0, -gravity)):
            self.hitbox.bottom = ground.rect.top
            if click:
                return self.change_gravity(gravity)
        
        if self.hitbox.colliderect(ceiling.rect.move(0, -gravity)):
            self.hitbox.top = ceiling.rect.bottom
            if click:
                return self.change_gravity(gravity)
        
        # Landen auf Level-Komponenten
        for sprite in level_gr:
            if sprite.type == "platform":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    if self.death_touch(gravity, sprite):
                        return DEATH
                    if gravity == 1:
                        self.hitbox.bottom = sprite.hitbox.top
                    else:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.vel = 0
                    if click:
                        return self.change_gravity(gravity)
            elif sprite.type == "hazard":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    return DEATH
            elif sprite.type == "pad":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    self.jump(gravity * PAD_VEL[sprite.color])
            elif sprite.type == "formportal":
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    if sprite.color == "green":
                        return CUBE_GAMEMODE
                    elif sprite.color == "magenta":
                        return SHIP_GAMEMODE
        
        self.angle = 0 if self.angle == 360 or self.angle == -360 else self.angle

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.hitbox.center)
        return super().update(*args, **kwargs) 


# Background-Sprites
class Ground(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(f"{ASSETS_FOLDER}/textures/bg/ground.jpg").convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH+UNIT, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = -UNIT, GROUND_HEIGHT


class Background(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(f"{ASSETS_FOLDER}/textures/bg/background.png").convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_HEIGHT*2*(16/9), SCREEN_HEIGHT*2))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, -SCREEN_HEIGHT/4
    
    def reset(self):
        self.rect.left, self.rect.top = 0, -SCREEN_HEIGHT/4

    def update(self, *args: Any, **kwargs: Any) -> None:
        # self.rect.x -= BACKGROUND_SCROLL_SPEED    # Bewegen des Hintergrunds nach links
        return super().update(*args, **kwargs)


class Ceiling(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(f"{ASSETS_FOLDER}/textures/bg/ground.jpg").convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = 0, 0

        self.activated = False
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.activated:
            if self.rect.bottom < CEILING_HEIGHT-CEILING_MOVE:
                self.rect.bottom += CEILING_MOVE
        else:
            if self.rect.bottom > -CEILING_MOVE:
                self.rect.bottom -= CEILING_MOVE
        return super().update(*args, **kwargs)


# Component-Sprite (für die Hindernisse im Spiel)
class Component(HitboxSprite):
    def __init__(self, imgfile=f"{ASSETS_FOLDER}/textures/transparent.png",
                 pos=None, size=None, angle=0, hb_mul=1.0, type_="deco", color="yellow",
                 *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image_filename = imgfile
        if pos is None:
            pos = [0.0, 0.0]
        if size is None:
            size = [1.0, 1.0]
        self.pos = pos
        self.size = size
        self.angle = angle
        self.hb_mul = hb_mul
        self.type = type_   # platform: Man kann darauf landen und davon abspringen
                            # hazard: Man stirbt, wenn man es berührt
                            # deco: Es zählt als Dekoration und wird vom Spieler ignioriert
                            # ring: Rings, von denen man abspringen kann, wenn man die Maustaste drückt
                            # gravportal: Portale, die die Gravitationsrichtung wechseln
                            # formportal: Portale, die den Spielmodus wechseln
        self.color = color  # Wird als Indentifikation für Rings und Portale verwendet.

        self.real_init()
    
    def real_init(self):
        self.original_image = pygame.image.load(self.image_filename).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (UNIT*self.size[0], UNIT*self.size[1]))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos[0]*UNIT, self.pos[1]*UNIT  # Position des Komponenten
        self.hitbox = self.image.get_rect()
        self.hitbox.x, self.hitbox.y = self.pos[0]*UNIT, self.pos[1]*UNIT
        self.hitbox.width, self.hitbox.height = \
            self.rect.width * self.hb_mul, self.rect.height * self.hb_mul
        # Der Hitbox kann um einen bestimmten Faktor vergrößert oder verkleinert werden

        self.rotate_sprite(self.angle)
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)
