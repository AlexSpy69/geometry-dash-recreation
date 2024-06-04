import pygame
from pygame.sprite import AbstractGroup
from geometry_dash_recreation.constants import *
from geometry_dash_recreation.assets import spritesheets
pygame.init()


class UIElement(pygame.sprite.Sprite):
    def __init__(self, filename: str, size: tuple, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/{filename}").convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


class PauseButton(UIElement):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__("pause_button.png", (UNIT, UNIT), *groups)
        self.rect.right, self.rect.top = SCREEN_WIDTH, 0


class Arrow(UIElement):
    def __init__(self, right: bool, *groups: AbstractGroup) -> None:
        super().__init__("arrow_left.png", (UNIT*1.5, UNIT*1.5), *groups)
        self.image = pygame.transform.flip(self.image, True, False) if right else self.image
        self.rect = self.image.get_rect()


class UserIcon(UIElement):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__("user_icon.png", (UNIT, UNIT), *groups)


class BuildIcon(UIElement):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__("build_icon.png", (UNIT, UNIT), *groups)


class ExitButton(UIElement):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__("exit_button.png", (UNIT*1.5, UNIT*1.5), *groups)


class PlusIcon(UIElement):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__("plus_icon.png", (UNIT, UNIT), *groups)


class TrashIcon(UIElement):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__("trash_icon.png", (UNIT, UNIT), *groups)


class EditIcon(UIElement):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__("edit_icon.png", (UNIT, UNIT), *groups)


class EditorIconsSheet(spritesheets.Spritesheet):
    def __init__(self):
        super().__init__(f"{ASSETS_FOLDER}/textures/ui/editor_icons.png")

    def get_image(self, rectangle: tuple) -> pygame.Surface:
        rectangle = [x * 32 for x in rectangle]
        return super().image_at(rectangle)


class EditorIcon(pygame.sprite.Sprite):
    def __init__(self, pos: list, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = EditorIconsSheet().get_image(pos)
        self.image = pygame.transform.scale(self.image, (UNIT, UNIT))
        self.rect = self.image.get_rect()


class EditorBarLabel(UIElement):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__("editor_bar_label.png", (SCREEN_WIDTH, SCREEN_HEIGHT-GROUND_HEIGHT), *groups)
