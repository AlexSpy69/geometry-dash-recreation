"""Modul mit den Sprites, die im Spiel verwendet werden können."""

from abc import ABC, abstractmethod

import pygame
from pygame.sprite import AbstractGroup
from geometry_dash_recreation import constants as const

pygame.init()


class HitboxSprite(pygame.sprite.Sprite):
    """
    Die Klasse für Sprites, neben pygame.sprite.Sprite die folgende Attribute besitzen sollen:

    * Dateiname
    * Initialer Rect
    * Hitbox-Rect
    * type-Attribut
    * color-Attribut
    * Winkel / Rotation

    Darüber hinaus besitzt diese Klasse zusätzliche Methoden.

    :var image_filename: Dateiname der Image-Datei
    :var original_image: pygame.Surface mit der unveränderten originalen Image-Datei
    :var image: pygame.Surface mit der Image-Datei, die auf den Bildschirm angezeigt wird und durch pygame.transform
    verändert wird
    :var initial_rect: pygame.Rect mit der initialen Position und Größe der Sprites
    :var rect: pygame.Rect mit der Position und Größe des Sprites
    :var hitbox: pygame.Rect mit der Position und Größe des Bereichs, der für die Kollisionsdetektierung verwendet wird
    :var type: type-Attribut des Sprites
    :var color: color-Attribut des Sprites
    :var angle: Winkel des Sprites
    """

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image_filename = ""
        self.original_image = pygame.Surface((0, 0))
        self.image = pygame.Surface((0, 0))
        self.initial_rect = pygame.Rect(0, 0, 0, 0)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.type = ""
        self.color = ""
        self.angle = 0

    def __str__(self) -> str:
        return (f"Type: {self.type}\nColor: {self.color}\nRect: {self.rect}\n"
                f"Hitbox: {self.hitbox}\nAngle: {self.angle}\n")

    def move_sprite(self, x: int, y: int) -> None:
        """
        Bewegt den Sprite. initial_rect wird nicht angepasst.

        :param x: Bewegung in die x-Richtung in Pixeln
        :param y: Bewegung in die y-Richtung in Pixeln
        :return:
        """

        self.rect.x += x
        self.rect.y += y
        self.hitbox.center = self.rect.center

    def move_initial(self, x: int, y: int) -> None:
        """
        Bewegt den Sprite. Die x- und y-Werte werden zu initial_rect addiert.

        :param x: Bewegung in die x-Richtung in Pixeln
        :param y: Bewegung in die y-Richtung in Pixeln
        :return:
        """

        self.move_sprite(x, y)
        self.initial_rect.x += x
        self.initial_rect.y += y

    def set_sprite_position(self, pos: tuple) -> None:
        """
        Setzt die Sprite-Position auf die Koordinaten in pos.

        :param pos: Tupel mit der x-Position als erstes und der y-Position als zweites Element
        :return:
        """

        self.rect.x, self.rect.y = pos
        self.hitbox.center = self.rect.center

    def rotate_sprite(self, angle: int) -> None:
        """
        Dreht den Sprite.

        :param angle: Winkel, um den der Sprite bewegt werden muss (in Grad)
        :return:
        """

        old_center = self.rect.center
        self.angle += angle
        self.angle %= 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=old_center)

    def smooth_angle(self, goal_angle: int = 0) -> None:
        """
        Dreht den Sprite mithilfe exponentieller Abnahme geschmeidig in einen bestimmten Winkel.

        :param goal_angle: Zielwinkel
        :return:
        """

        dif = self.angle - goal_angle
        self.angle -= dif / 2
        if round(dif, 1) == 0:
            self.angle = goal_angle


# Spieler-Sprites
class Gamemode(ABC, HitboxSprite):
    """
    Abstrakte Basisklasse für Spielmodus-Sprites. Diese haben neben HitboxSprite ein Velocity-Attribut, das die
    gesamte Spielphysik ausmacht.

    Darüber hinaus besitzt diese Klasse zusätzliche Methoden.

    :var vel: Velocity-Attribut
    """

    def __init__(self, filename: str, *groups: AbstractGroup) -> None:
        """
        Konstruktormethode von Gamemode.

        :param filename: Dateiname der Imagedatei, die als Textur verwendet werden soll.
        :param groups: Pygame-Gruppen, in denen der Sprite enthalten sein soll.
        """

        super().__init__(*groups)
        self.original_image = pygame.image.load(f"{const.ASSETS_FOLDER}/textures/icons/{filename}").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (const.UNIT, const.UNIT))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.right, self.rect.bottom = const.PLAYER_X, const.PLAYER_Y
        self.hitbox = self.image.get_rect()
        self.hitbox.right, self.hitbox.bottom = const.PLAYER_X, const.PLAYER_Y

        self.image_filename = f"{const.ASSETS_FOLDER}/textures/icons/{filename}"
        self.vel = 0
        self.angle = 0

    def reset(self) -> None:
        """
        Setzt Werte zu Winkel, Velocity und Position auf ihre initialen Werte zurück.

        :return:
        """

        self.angle = 0
        self.vel = 0
        self.hitbox.right, self.hitbox.bottom = 0, const.PLAYER_Y

    def jump(self, mul: int) -> None:
        """
        Lässt den Spieler springen.

        :param mul: Sprunghöhe
        :return:
        """

        self.vel = -const.JUMP_VEL * mul

    def death_touch(self, gravity: int, sprite: pygame.sprite.Sprite) -> bool:
        """
        Bestimmt, ob der Spieler sterben soll.

        :param gravity: Gravitationsrichtung
        :param sprite: Spielsprite, den der Spieler berührt hat
        :return: Der Bool-Wert
        """

        if gravity == 1:
            return self.hitbox.bottom - const.DEATH_ACCURACY >= sprite.hitbox.top
        elif gravity == -1:
            return self.hitbox.top + const.DEATH_ACCURACY <= sprite.hitbox.bottom

    @abstractmethod
    def controls(self, ev: bool, click: bool, gravity: int, ground: pygame.sprite.Sprite, ceiling: pygame.sprite.Sprite,
                 level_gr: pygame.sprite.Group, level_gr_unconverted: dict) -> int:
        """
        Abstrakte Methode für die Controls des Gamemodes (die für jede Subklasse anders implementiert wird).
        Wenn diese Methode von gdr.base aufgerufen wird, sind die Parameter in Wirklichkeit Variablen aus gdr.base, die
        für die Physik des Gamemode-Sprites benötigt werden.

        :param ev: Ist die Maustaste des Spielers gerade gedrückt?
        :param click: Hat der Spieler im aktuellen Frame die Maustaste gedrückt?
        :param gravity: Die Gravitationsrichtung
        :param ground: Der Boden-Sprite
        :param ceiling: Der Decken-Sprite
        :param level_gr: Die Level-Spritegruppe
        :param level_gr_unconverted: Das Leveldaten-Dictionary von level_gr
        :return: Exit-Code (Mögliche Werte: NORMAL, DEATH, WIN, CHANGE_GRAVITY, CUBE_GAMEMODE, SHIP_GAMEMODE,
        BALL_GAMEMODE)
        """

        pass

    def update(self) -> None:
        """
        Passt die Image-Datei und den Rect des Sprites an das Winkel-Attribut an.
        :return:
        """

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.hitbox.center)


class Cube(Gamemode):
    """
    Subklasse von gdr.game_sprites.Gamemode für den Cube-Gamemode (mit Implementation der controls-Methode).
    """

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__("cubes/icon_1.png", *groups)

    def controls(self, ev: bool, click: bool, gravity: int, ground: pygame.sprite.Sprite, ceiling: pygame.sprite.Sprite,
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
                            self.vel = -gravity * const.JUMP_VEL / 1.5
                            return const.CHANGE_GRAVITY
                        self.jump(gravity * const.RING_VEL[sprite.color])

        # Einwirkung der Gravitation
        self.hitbox.y += self.vel * const.DELTA_TIME * const.RESIZE
        self.vel += const.VEL_ADD * gravity * const.DELTA_TIME

        self.angle -= gravity * 7 * const.DELTA_TIME

        if self.hitbox.y < const.OUT_OF_BOUNDS:
            return const.DEATH

        # Landen auf dem Boden
        if self.hitbox.colliderect(ground.rect.move(0, -gravity)):
            if gravity == -1:
                return const.DEATH
            self.angle = round(self.angle / 90) * 90
            self.hitbox.bottom = ground.rect.top
            self.vel = 0

        # Landen auf Level-Komponenten
        for sprite in level_gr:
            if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                match sprite.type:
                    case "platform":
                        if self.death_touch(gravity, sprite):
                            return const.DEATH
                        self.angle = round(self.angle / 90) * 90
                        if gravity == 1:
                            self.hitbox.bottom = sprite.hitbox.top
                        elif gravity == -1:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.vel = 0
                    case "hazard":
                        return const.DEATH
                    case "pad":
                        self.jump(gravity * const.PAD_VEL[sprite.color])
                    case "formportal":
                        match sprite.color:
                            case "magenta":
                                return const.SHIP_GAMEMODE
                            case "red":
                                return const.BALL_GAMEMODE

        self.angle = 0 if self.angle == 360 or self.angle == -360 else self.angle

        return const.NORMAL


class Ship(Gamemode):
    """
    Subklasse von gdr.game_sprites.Gamemode für den Ship-Gamemode (mit Implementation der controls-Methode).
    """

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__("ships/ship_01.png", *groups)
        self.upsidedown = False

    def flip(self) -> None:
        """
        Dreht den Image des Ships für den Gravitationswechsel um und passt auch das Attribut vel an.

        :return:
        """

        self.upsidedown = not self.upsidedown
        y = self.rect.y
        x = self.rect.x
        self.original_image = pygame.transform.flip(self.original_image, False, True)
        self.rect = self.original_image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.vel = -self.vel

    def controls(self, ev: bool, click: bool, gravity: int, ground: pygame.sprite.Sprite, ceiling: pygame.sprite.Sprite,
                 level_gr: pygame.sprite.Group, level_gr_unconverted: dict) -> int:
        if click:
            for sprite in level_gr:
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    if sprite.type == "ring":
                        if sprite.color == "cyan":
                            # self.vel = -gravity * const.JUMP_VEL / 1.5
                            self.flip()
                            return const.CHANGE_GRAVITY
                        self.jump(gravity * const.RING_VEL[sprite.color])

        # Einwirkung der Gravitation
        self.hitbox.y += self.vel * const.DELTA_TIME * const.RESIZE

        # Fliegen
        if ev:
            self.vel -= const.VEL_ADD * gravity * const.DELTA_TIME / 2
        else:
            self.vel += const.VEL_ADD * gravity * const.DELTA_TIME / 2

        self.vel = -20 if self.vel <= -20 else self.vel
        self.vel = 20 if self.vel >= 20 else self.vel

        # Landen auf dem Boden
        if self.hitbox.colliderect(ground.rect.move(0, -gravity)):
            self.smooth_angle()
            self.hitbox.bottom = ground.rect.top
            if gravity == 1 and not ev:
                self.vel = 0
            elif gravity == 0 and ev:
                self.vel = 0
        elif self.hitbox.colliderect(ceiling.rect.move(0, -gravity)):
            self.smooth_angle()
            self.hitbox.top = ceiling.rect.bottom - 1
            if gravity == 1 and ev:
                self.vel = 0
            elif gravity == 0 and not ev:
                self.vel = 0
        else:
            self.angle = -self.vel * 2

        # Landen auf Level-Komponenten
        for sprite in level_gr:
            if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                match sprite.type:
                    case "platform":
                        normal_death = self.death_touch(gravity, sprite)
                        upside_down_death = self.death_touch(-gravity, sprite)
                        if normal_death and upside_down_death:
                            return const.DEATH
                        self.smooth_angle()
                        if not normal_death or not upside_down_death:
                            self.vel = 0
                    case "hazard":
                        return const.DEATH
                    case "pad":
                        self.jump(gravity * const.PAD_VEL[sprite.color])
                    case "formportal":
                        match sprite.color:
                            case "green":
                                return const.CUBE_GAMEMODE
                            case "red":
                                return const.BALL_GAMEMODE

        return const.NORMAL


class Ball(Gamemode):
    """
    Subklasse von gdr.game_sprites.Gamemode für den Ball-Gamemode (mit Implementation der controls-Methode).
    """

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__("balls/ball_1.png", *groups)

    def jump(self, mul: int) -> None:
        self.vel = -const.JUMP_VEL * mul * 0.7

    def change_gravity(self, gravity: int) -> int:
        """
        Passt das Attribut vel für den Gravitationswechsel an.

        :param gravity: Gravitationsrichtung
        :return: Konstante CHANGE_GRAVITY
        """
        self.vel = const.VEL_ADD * -gravity * 5
        return const.CHANGE_GRAVITY

    def controls(self, ev: bool, click: bool, gravity: int, ground: pygame.sprite.Sprite, ceiling: pygame.sprite.Sprite,
                 level_gr: pygame.sprite.Group, level_gr_unconverted: dict) -> int:
        if click:
            for sprite in level_gr:
                if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                    if sprite.type == "ring":
                        if sprite.color == "cyan":
                            # self.vel = -gravity * const.JUMP_VEL / 1.5
                            return self.change_gravity(gravity)
                        self.jump(gravity * const.RING_VEL[sprite.color])

        # Einwirkung der Gravitation
        self.hitbox.y += self.vel * const.DELTA_TIME * const.RESIZE

        self.vel += const.VEL_ADD * gravity * const.DELTA_TIME / 2

        self.vel = -40 if self.vel <= -40 else self.vel
        self.vel = 40 if self.vel >= 40 else self.vel

        self.angle -= const.VEL_ADD * gravity * 4 * const.DELTA_TIME

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
            if self.hitbox.colliderect(sprite.hitbox.move(0, -gravity)):
                match sprite.type:
                    case "platform":
                        if self.death_touch(gravity, sprite):
                            return const.DEATH
                        if gravity == 1:
                            self.hitbox.bottom = sprite.hitbox.top
                        else:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.vel = 0
                        if click:
                            return self.change_gravity(gravity)
                    case "hazard":
                        return const.DEATH
                    case "pad":
                        self.jump(gravity * const.PAD_VEL[sprite.color])
                    case "formportal":
                        match sprite.color:
                            case "green":
                                return const.CUBE_GAMEMODE
                            case "magenta":
                                return const.SHIP_GAMEMODE

        self.angle = 0 if self.angle == 360 or self.angle == -360 else self.angle

        return const.NORMAL


# Background-Sprites
class Ground(pygame.sprite.Sprite):
    """
    Sprite-Klasse für den Boden im Spiel.
    """

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(f"{const.ASSETS_FOLDER}/textures/bg/ground.jpg").convert()
        self.image = pygame.transform.scale(self.image, (const.SCREEN_WIDTH + const.UNIT, const.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = -const.UNIT, const.GROUND_HEIGHT


class Background(pygame.sprite.Sprite):
    """
    Sprite-Klasse für den Hintergrund im Spiel.
    """

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(f"{const.ASSETS_FOLDER}/textures/bg/background.png").convert()
        self.image = pygame.transform.scale(self.image, (const.SCREEN_HEIGHT * 2 * (16 / 9),
                                                         const.SCREEN_HEIGHT * 2))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, -const.SCREEN_HEIGHT / 4

    def reset(self):
        self.rect.left, self.rect.top = 0, -const.SCREEN_HEIGHT / 4


class Ceiling(pygame.sprite.Sprite):
    """
    Sprite-Klasse für die Decke im Spiel.
    """

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(f"{const.ASSETS_FOLDER}/textures/bg/ground.jpg").convert()
        self.image = pygame.transform.scale(self.image, (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = 0, 0

        self.activated = False

    def update(self) -> None:
        """
        Lässt die Decke ab, falls das Attribut activated True ist, und bewegt sie wieder nach oben, wenn activated
        False ist.

        :return:
        """

        if self.activated:
            if self.rect.bottom < const.CEILING_HEIGHT - const.CEILING_MOVE:
                self.rect.bottom += const.CEILING_MOVE
        else:
            if self.rect.bottom > -const.CEILING_MOVE:
                self.rect.bottom -= const.CEILING_MOVE


# Component-Sprite (für die Hindernisse im Spiel)
class Component(HitboxSprite):
    """
    Klasse für die Level-Komponenten.

    :var image_filename: Dateiname der Image-Datei, die als Textur verwendet werden soll.
    :var pos: Tupel mit der Position des Sprites in UNIT.
    :var size: Größe des Sprites in UNIT.
    :var angle: Winkel des Sprites in Grad.
    :var hb_mul: Verhältnis der Größe von hitbox zur Größe von rect.
    :var type: Typ der Komponente.
    :var color: Farbe der Komponente.
    """

    def __init__(self, imgfile=f"{const.ASSETS_FOLDER}/textures/transparent.png",
                 pos: tuple = None, size: tuple = None, angle=0, hb_mul=1.0, type_="deco", color="yellow",
                 *groups: AbstractGroup) -> None:
        """
        Konstruktormethode von Component.

        :param imgfile: Dateiname der Image-Datei, die als Textur verwendet werden soll.
        :param pos: Tupel mit der Position des Sprites in UNIT.
        :param size: Größe des Sprites in UNIT.
        :param angle: Winkel des Sprites in Grad.
        :param hb_mul: Verhältnis der Größe von hitbox zur Größe von rect.
        :param type_: Initialisierungswert des Attributs type.
        :param color: Initialisierungswert des Attributs color.
        :param groups: Die Spritegruppen, in die dieser Sprite enthalten sein soll.
        """

        super().__init__(*groups)
        self.image_filename = imgfile
        if pos is None:
            pos = [0.0, 0.0]
        if size is None:
            size = [1.0, 1.0]
        # Positions-Attribut
        self.pos = pos
        # Größen-Attribut (in UNIT)
        self.size = size
        # Rotation/Winkel-Attribut
        self.angle = angle
        # Attrbut zum Verhältnis der Größe des Sprites (rect) und der des Hitboxes (hitbox)
        self.hb_mul = hb_mul
        # Typ-Attribut des Level-Komponenten
        self.type = type_
        # Farben-Attribut des Level-Komponenten: Wird als Indentifikation für Rings und Portale verwendet.
        self.color = color

        self.real_init()

    def real_init(self):
        """
        Neubestimmung der Attribute original_image, image, rect, initial_rect und hitbox anhand der Werte in den
        Attributen pos, size, angle, hb_mul, type und color. Wird auch von __init__ aufgerufen.

        :return:
        """

        self.original_image = pygame.image.load(self.image_filename).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (const.UNIT * self.size[0],
                                                                           const.UNIT * self.size[1]))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos[0] * const.UNIT, self.pos[1] * const.UNIT  # Position des Komponenten
        self.initial_rect = self.image.get_rect()
        self.initial_rect.x, self.initial_rect.y = self.pos[0] * const.UNIT, self.pos[1] * const.UNIT
        self.hitbox = self.image.get_rect()
        self.hitbox.x, self.hitbox.y = self.pos[0] * const.UNIT, self.pos[1] * const.UNIT
        self.hitbox.width, self.hitbox.height = \
            self.rect.width * self.hb_mul, self.rect.height * self.hb_mul
        # Der Hitbox kann um einen bestimmten Faktor vergrößert oder verkleinert werden

        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=old_center)
