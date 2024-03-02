import pickle
from geometry_dash_recreation.level import level


class SaveFile(object):
    def __init__(self):
        self.playerdata = {'name': 'Player'}
        self.playerstats = {'stars': 0}
        self.lvldict = {}
    
    def __str__(self) -> str:
        return f'Player Data: {self.playerdata}\nPlayer Stats: {self.playerstats}\nLevels: {self.lvldict}'
    
    def set_level(self, filename, percent) -> None:
        self.lvldict[filename] = percent

    def get_level_percent(self, filename) -> int:
        try:
            return self.lvldict[filename]
        except KeyError:
            return 0
    
    def update_stats(self) -> None:
        for cat in self.playerstats.keys():
            self.playerstats[cat] = 0
        for lvl in self.lvldict.keys():
            try:
                lvlinfo = level.open_level_data(lvl)["info"]
                self.playerstats["stars"] += int(lvlinfo["stars"])
            except FileNotFoundError:
                pass


def save_sf(obj: SaveFile, fn) -> None:
    with open(fn, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
        outp.close()


def open_sf(fn) -> SaveFile:
    try:
        with open(fn, 'rb') as inp:
            return pickle.load(inp)
    except FileNotFoundError or EOFError:
        save_sf(SaveFile(), fn)
        return open_sf(fn)


def truncate_sf(fn) -> None:
    with open(fn, 'wb') as outp:
        pickle.dump(SaveFile(), outp, pickle.HIGHEST_PROTOCOL)
        outp.close()
