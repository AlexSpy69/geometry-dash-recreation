"""Dieses Modul enthält Funktionen, die an mehreren Stellen im Spiel verwendet werden, aber keine Verbindung zu
pygame haben."""

import os
from typing import Any


def list_files(directory: str, extenstion: str = "") -> list:
    """
    Liefert eine Liste mit allen Dateien in einem Ordner.

    :param directory: Name des Ordners
    :param extenstion: Erlaubte Dateiendung

    :return: Liste mit den Dateinamen
    """

    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extenstion):
                file_list.append(os.path.join(root, file))
    return file_list


def try_float(value: Any) -> Any:
    """
    Versucht, einen Wert zu float zu konvertieren.

    :param value: Beliebiger Wert
    :return: Konversion zu Float bei Erfolg; ansonsten unveränderter Wert
    """

    try:
        return float(value)
    except ValueError:
        return value


def try_detuple(t: tuple) -> Any:
    """
    Liefert das einzige Element aus einem Tupel, falls es nur ein Element enthält.

    :param t: Das Tupel
    :return: t[0] falls len(t) == 1 sonst t
    """

    return t[0] if len(t) == 1 else t


def csv_reader(filename: str, line_single: bool = True) -> tuple:
    """
    Liest eine CSV-Datei und gibt ein zweidimensionales Tupel mit dem Inhalt zurück. Das Haupttupel enthält mehrere
    Tupel für jede CSV-Zeile, die die von Kommas getrennten CSV-Werte enthalten.

    :param filename: Dateiname der CSV-Datei
    :param line_single: Sollen CSV-Zeilen mit nur einem Element direkt zum Haupttupel hinzugefügt werden?
    :return:
    """

    output_list = []
    with open(filename) as f:
        for line in f.readlines():
            add = tuple(map(try_float, line.rstrip("\n").split(",")))
            add = try_detuple(add) if line_single else add
            output_list.append(add)
    return tuple(output_list)


def iter_add(x: tuple | list, y: tuple | list) -> list:
    """
    Addiert die Elemente mit dem selben Index aus zwei Tupeln oder Listen und liefert eine Liste mit den Ergebnissen,
    die den entsprechenden Index haben.

    :param x: Das erste Tupel / die erste Liste
    :param y: Das erste Tupel / die erste Liste
    :return: Liste mit den addierten Werten aus x und y
    """

    r = []
    for i in range(0, len(x)):
        r.append(x[i] + y[i])
    return r
