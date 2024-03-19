from turtle import position
import pygame
from geometry_dash_recreation.assets import game_sprites
from geometry_dash_recreation.constants import *

pygame.init()


class Level(dict):
    def __init__(self) -> None:
        super().__init__()
        self["info"] = {"name": "",
                        "creator": "",
                        "stars": "0"}
        self["data"] = {"gamemode": "cube",
                        "song": ""}
        self["sprites"] = []


class CompSprite(dict):
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


def round_position(pos: list, spritetype: str):
    if spritetype == "pad":
        return [round(pos[0], 1), round(pos[1], 1)]
    return [round(pos[0]), round(pos[1])]


def round_size(size: list, spritetype: str):
    if spritetype in ("formportal", "pad"):
        return [round(size[0], 1), round(size[1], 1)]
    return [round(size[0]), round(size[1])]


def data_to_sprite(data: CompSprite) -> game_sprites.Component:
    return game_sprites.Component(imgfile=data["imgfile"], pos=data["pos"],
                                  size=data["size"], angle=data["angle"], hb_mul=data["hb_mul"],
                                  type_=data["type"], color=data["color"])


def data_to_group(data: Level) -> pygame.sprite.Group:
    gr = pygame.sprite.Group()
    for element in data["sprites"]:
        gr.add(data_to_sprite(element))
    return gr


def sprite_to_data(sprite: game_sprites.Component) -> CompSprite:
    return CompSprite(imgfile=sprite.image_filename, pos=round_position([sprite.rect.x/UNIT, sprite.rect.y/UNIT], sprite.type),
                      size=round_size([sprite.rect.width/UNIT, sprite.rect.height/UNIT], sprite.type), angle=sprite.angle,
                      hb_mul=sprite.hitbox.width / sprite.rect.width, type_=sprite.type, color=sprite.color)
