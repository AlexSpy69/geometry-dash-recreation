from typing import Any
import pygame
from pygame.sprite import AbstractGroup
from geometry_dash_recreation.constants import *
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
