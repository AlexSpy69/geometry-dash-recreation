import pickle
import pygame
from geometry_dash_recreation.constants import *
import geometry_dash_recreation.convert as convert

pygame.init()

# Auslesen der Leveldaten aus einer Datei
def open_level_data(filename: str) -> convert.Level:
    with open(filename, "rb") as f:
        return pickle.load(f)

# Auslesen der Leveldaten aus einer Datei und Konvertieren zu pygame.sprite.Group
def open_level(filename: str) -> pygame.sprite.Group:
    return convert.data_to_group(open_level_data(filename))

# Schreiben von Leveldaten in eine Datei
def save_level_data(filename: str, group: convert.Level) -> None:
    with open(filename, "wb") as f:
        pickle.dump(group, f)
