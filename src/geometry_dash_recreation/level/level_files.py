"""Modul, das für das Öffnen und Speichern von Leveldateien zuständig ist."""

import pickle
import pygame
from geometry_dash_recreation.level import convert

pygame.init()


def open_level_data(filename: str) -> convert.Level:
    """
    Liest ein Leveldaten-Dictionary aus einer Leveldatei.

    :param filename: Dateiname
    :return: gdr.level.convert.Level-Objekt
    """

    with open(filename, "rb") as f:
        return pickle.load(f)


def open_level(filename: str) -> pygame.sprite.Group:
    """
    Liest ein Leveldaten-Dictionary aus einer Leveldatei und konvertiert es direkt zu einer Pygame-Spritegruppe.

    :param filename: Dateiname
    :return: pygame.sprite.Group-Objekt
    """

    return convert.data_to_group(open_level_data(filename))


def save_level_data(filename: str, data: convert.Level) -> None:
    """
    Speichert ein Leveldaten-Dictionary in eine Datei.

    :param filename: Dateiname
    :param data: gdr.level.convert.Level-Objekt
    :return:
    """

    with open(filename, "wb") as f:
        pickle.dump(data, f)
