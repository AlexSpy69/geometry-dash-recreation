"""Das Modul, das für das Umgehen mit Save-Files zuständig ist."""

import pickle
from geometry_dash_recreation.level import level_files


class SaveFile(object):
    """
    Klasse für das Save-File.

    :var playerdata: Dictionary mit den persönlichen Daten des Spielers (Keys: "name" -> str)
    :var playerstats: Dictionary mit den Spielstatistiken des Spielers (Keys: "stars" -> int)
    :var lvldict: Dictionary mit den von dem Spieler bisher gespielten Levels als Keys (str) und dem höchsten erreichten
        Prozentsatz als zugehöriger Wert (int)
    """

    def __init__(self):
        self.playerdata = {'name': 'Player'}
        self.playerstats = {'stars': 0}
        self.lvldict = {}
    
    def __str__(self) -> str:
        return f'Player Data: {self.playerdata}\nPlayer Stats: {self.playerstats}\nLevels: {self.lvldict}'
    
    def set_level(self, filename: str, percent: int) -> None:
        """
        Speichert ein Level und den zugehörigen Prozentsatz ein.

        :param filename: Dateiname der Leveldatei
        :param percent: Prozentsaetz
        :return:
        """

        self.lvldict[filename] = percent

    def get_level_percent(self, filename: str) -> int:
        """
        Liefert den Prozentsatz, den der Spieler in einem Level erreicht hat.

        :param filename: Dateiname der Leveldatei
        :return: Zugehöriger Prozentsatz, falls das Level jemals bisher gespielt wurde; ansonsten 0
        """

        try:
            return self.lvldict[filename]
        except KeyError:
            return 0
    
    def update_stats(self) -> None:
        """
        Aktualisiert die Statistiken.

        :return:
        """

        for cat in self.playerstats.keys():
            self.playerstats[cat] = 0
        for lvl in self.lvldict.keys():
            try:
                lvlinfo = level_files.open_level_data(lvl)["info"]
                self.playerstats["stars"] += int(lvlinfo["stars"])
            except FileNotFoundError:
                pass


def save_sf(obj: SaveFile, fn: str) -> None:
    """
    Speichert ein SaveFile-Objekt in eine Datei.

    :param obj: SaveFile-Objekt
    :param fn: Name der Zieldatei
    :return:
    """

    with open(fn, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def open_sf(fn: str) -> SaveFile:
    """
    Öffnet ein SaveFile-Objekt aus einer Datei.

    :param fn:
    :return: SaveFile-Objekt
    """

    try:
        with open(fn, 'rb') as inp:
            return pickle.load(inp)
    except FileNotFoundError or EOFError:
        save_sf(SaveFile(), fn)
        return open_sf(fn)


def truncate_sf(fn: str) -> None:
    """
    Überschreibt eine SaveFile-Datei mit einem leeren SaveFile-Objekt.

    :param fn: Name der Zieldatei
    :return:
    """

    with open(fn, 'wb') as outp:
        pickle.dump(SaveFile(), outp, pickle.HIGHEST_PROTOCOL)
