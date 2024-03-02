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
    def __init__(self, imgfile="assets/textures/transparent.png",
                 pos=None, size=None, hb_mul=1.0, type_="deco", color="yellow") -> None:
        super().__init__()
        if pos is None:
            pos = [0, 0]
        if size is None:
            size = [1, 1]
        self["imgfile"] = imgfile
        self["pos"] = pos
        self["size"] = size
        self["hb_mul"] = hb_mul
        self["type"] = type_
        self["color"] = color


def data_to_sprite(data: CompSprite) -> game_sprites.Component:
    return game_sprites.Component(imgfile=data["imgfile"], pos=data["pos"],
                             size=data["size"], hb_mul=data["hb_mul"],
                             type_=data["type"], color=data["color"])


def data_to_group(data: Level) -> pygame.sprite.Group:
    gr = pygame.sprite.Group()
    for element in data["sprites"]:
        gr.add(data_to_sprite(element))
    return gr
