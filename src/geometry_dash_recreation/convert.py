import pygame
from geometry_dash_recreation.constants import *
import geometry_dash_recreation.sprites as sprites

pygame.init()

class Level(dict):
    def __init__(self) -> None:
        super().__init__()
        self["info"] = {"name": "",
                        "creator": "",
                        "difficulty": ""}
        self["data"] = {"gamemode": "cube",
                        "song": ""}
        self["sprites"] = []

class CompSprite(dict):
    def __init__(self, imgfile="assets/textures/transparent.png",
                 pos=[0, 0], size=[1, 1], hb_mul=1.0, type="deco", color="yellow") -> None:
        super().__init__()
        self["imgfile"] = imgfile
        self["pos"] = pos
        self["size"] = size
        self["hb_mul"] = hb_mul
        self["type"] = type
        self["color"] = color


def data_to_sprite(data: CompSprite) -> sprites.Component:
    return sprites.Component(imgfile=data["imgfile"], pos=data["pos"],
                             size=data["size"], hb_mul=data["hb_mul"],
                             type=data["type"], color=data["color"])


def data_to_group(data: Level) -> pygame.sprite.Group:
    gr = pygame.sprite.Group()
    for element in data["sprites"]:
        gr.add(data_to_sprite(element))
    return gr
