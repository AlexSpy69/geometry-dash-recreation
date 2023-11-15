import typing
import pickle
from typing import Any
import pygame
from geometry_dash_recreation.constants import *
import geometry_dash_recreation.sprites as sprites

pygame.init()

class LevelGroup(pygame.sprite.Group):
    def __init__(self, *sprites: pygame.sprite.Sprite | typing.Sequence[pygame.sprite.Sprite]) -> None:
        super().__init__(*sprites)
        self.info = {"name": "",
                     "creator": "",
                     "difficulty:": ""}
        self.data = {"gamemode": "cube",
                     "song": ""}
    
    def move_all(self, x=0, y=0) -> None:
        for sprite in self:
            sprite.rect.x += x
            sprite.rect.y += y

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.move_all(x=-LEVEL_SCROLL_SPEED)
        return super().update(*args, **kwargs)

# Auslesen eines Levels aus einer Datei
def open_level(filename: str) -> LevelGroup:
    with open(filename, "rb") as f:
        return pickle.load(f)

# Schreiben eines Levels in eine Datei
def save_level(filename: str, group: LevelGroup) -> None:
    with open(filename, "wb") as f:
        pickle.dump(group, f)
