from typing import Any
import pygame
from pygame.sprite import AbstractGroup
from geometry_dash_recreation.constants import *
from geometry_dash_recreation.assets import spritesheets
pygame.init()


# Sprite für den Pause-Knopf
class PauseButton(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/pause_button.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (UNIT, UNIT))
        self.rect = self.image.get_rect()
        self.rect.right, self.rect.top = SCREEN_WIDTH, 0
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, right: bool, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/arrow_left.png").convert_alpha()
        self.image = pygame.transform.flip(self.image, True, False) if right else self.image
        self.image = pygame.transform.scale(self.image, (UNIT*1.5, UNIT*1.5))
        self.rect = self.image.get_rect()
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)


class UserIcon(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/user_icon.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (UNIT, UNIT))
        self.rect = self.image.get_rect()
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)


class BuildIcon(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/build_icon.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (UNIT, UNIT))
        self.rect = self.image.get_rect()
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)


class ExitButton(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/exit_button.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (UNIT*1.5, UNIT*1.5))
        self.rect = self.image.get_rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)


class EditorIconsSheet(spritesheets.spritesheet):
    def __init__(self):
        super().__init__(f"{ASSETS_FOLDER}/textures/ui/editor_icons.png")

    def image_at(self, rectangle, colorkey=None):
        rectangle = [x * 32 for x in rectangle]
        return super().image_at(rectangle, colorkey)


class EditorIcon(pygame.sprite.Sprite):
    def __init__(self, pos: list, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = EditorIconsSheet().image_at(pos)
        self.image = pygame.transform.scale(self.image, (UNIT, UNIT))
        self.rect = self.image.get_rect()
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)
