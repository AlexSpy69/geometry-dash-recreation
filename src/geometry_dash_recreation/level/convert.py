"""Modul zum Konvertieren von Daten-Dictionarys zu Pygame-Objekten und zurück."""

import pygame
from geometry_dash_recreation.assets import game_sprites
from geometry_dash_recreation.constants import UNIT, ASSETS_FOLDER

pygame.init()


class Level(dict):
    """
    Subklasse von dict, die eine vordefinierte Struktur hat:

    {
        "info": {"name": "", "creator": "", "stars": "0"},

        "data": {"gamemode": "cube", "song": ""}

        "sprites": []
    }

    Anmerkung: Der song-Key wird in der aktuellen Version des Spiels nicht verwendet!
    """

    def __init__(self) -> None:
        super().__init__()
        self["info"] = {"name": "",
                        "creator": "",
                        "stars": "0"}
        self["data"] = {"gamemode": "cube",
                        "song": ""}    # noch unbenutzt!
        self["sprites"] = []


class CompSprite(dict):
    """
    Subklasse von dict, die eine vordefinierte Struktur hat:

    {
        "imgfile": "some_image.png",

        "pos": [0, 0],

        "size": [1, 1],

        "angle": 0,

        "hb_mul": 2,

        "type": ring,

        "color": yellow
    }
    """

    def __init__(self, imgfile=f"{ASSETS_FOLDER}/textures/transparent.png",
                 pos=None, size=None, angle=0, hb_mul=1.0, type_="deco", color="yellow") -> None:
        super().__init__()
        if pos is None:
            pos = [0, 0]
        if size is None:
            size = [1, 1]
        self["imgfile"] = imgfile
        self["pos"] = pos
        self["size"] = size
        self["angle"] = angle
        self["hb_mul"] = hb_mul
        self["type"] = type_
        self["color"] = color


def round_position(pos: list, spritetype: str) -> list:
    """
    Rundet eine Sprite-Position.

    :param pos: Alte Sprite-Position [x, y]
    :param spritetype: type-Attribut des Sprites
    :return: Neue Sprite-Position [x, y]
    """

    if spritetype == "pad":
        return [round(pos[0], 1), round(pos[1], 1)]
    return [round(pos[0]), round(pos[1])]


def round_size(size: list, spritetype: str) -> list:
    """
    Rundet eine Sprite-Größe.

    :param size: Alte Sprite-Größe [w, h]
    :param spritetype: type-Attribut des Sprites
    :return: Neue Sprite-Größe [w, h]
    """

    if spritetype in ("gravityportal", "formportal", "pad"):
        return [round(size[0], 1), round(size[1], 1)]
    return [round(size[0]), round(size[1])]


def data_to_sprite(data: CompSprite) -> game_sprites.Component:
    """
    Erzeugt ein gdr.assets.game_sprites.Component-Objekt aus den angegebenen Komponentendaten.

    :param data: Dictionary mit Kopmonentendaten (gdr.level.convert.CompSprite)
    :return: Komponenten-Objekt
    """

    return game_sprites.Component(imgfile=data["imgfile"], pos=data["pos"],
                                  size=data["size"], angle=data["angle"], hb_mul=data["hb_mul"],
                                  type_=data["type"], color=data["color"])


def data_to_group(data: Level) -> pygame.sprite.Group:
    """
    Erzeugt eine Pygame-Spritegruppe aus den angegebenen Leveldaten.

    :param data: Dictionary mit Leveldaten (gdr.level.convert.Level)
    :return: Pygame-Spritegruppe
    """

    gr = pygame.sprite.Group()
    for element in data["sprites"]:
        gr.add(data_to_sprite(element))
    return gr


def sprite_to_data(sprite: game_sprites.Component, use_initial_rect: bool = False) -> CompSprite:
    """
    Erzeugt ein Dictionary mit Komponentendaten aus einem Komponenten-Objekt.

    :param sprite: Komponenten-Objekt
    :param use_initial_rect: Soll für die Positionsangabe das Attribut initial_rect statt rect verwendet werden?
    :return: Komponentendaten-Dictionary (gdr.level.convert.CompSprite)
    """

    return CompSprite(imgfile=sprite.image_filename,
                      pos=round_position([sprite.rect.x/UNIT, sprite.rect.y/UNIT] if not use_initial_rect else
                                         [sprite.initial_rect.x/UNIT, sprite.initial_rect.y/UNIT], sprite.type),
                      size=round_size([sprite.rect.width/UNIT, sprite.rect.height/UNIT], sprite.type),
                      angle=sprite.angle,
                      hb_mul=sprite.hitbox.width / sprite.rect.width,
                      type_=sprite.type,
                      color=sprite.color)


def group_to_data(level_gr: pygame.sprite.Group, use_initial_rect: bool = False) -> list:
    """
    Erzeugt eine Liste mit gdr.level.convert.CompSprite-Objekten aus einem pygame.sprite.Group-Objekt. Diese kann
    für den "sprites"-Key von gdr.level.convert.Level verwendet werden.

    :param level_gr: Pygame-Spritegruppe
    :param use_initial_rect: Soll für die Positionsangaben das Attribut initial_rect statt rect verwendet werden?
    :return: Liste mit Komponentendaten-Dictionarys (gdr.level.convert.CompSprite)
    """

    dgr = []
    for sprite in level_gr:
        dgr.append(sprite_to_data(sprite, use_initial_rect))
    return dgr
