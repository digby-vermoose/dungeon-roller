#!/usr/bin/python3
import datetime
import argparse
from random import seed
from random import randint

class Dungeon:
    def __init__(self, name, paths):
        self.name = name
        self.paths = paths # list of paths

class Path:
    def __init__(self, name, number, difficulty):
        self.name = name
        self.number = number
        self.difficulty = difficulty # 1-3, 1 is easy, 3 is hard

class DungeonPath:
    def __init__(self, dungeon, path):
        self.dungeon = dungeon
        self.path = path

    def str(self):
        return "{:20s} - Path {:d} ({:s})".format(self.dungeon.name, self.path.number, self.path.name)

default_easy_paths = 3
default_medium_paths = 2
default_hard_paths = 1


ac_s = Path("Story",       0, 1)
ac_1 = Path("Hodgins",     1, 1)
ac_2 = Path("Detha",       2, 2)
ac_3 = Path("Tzark",       3, 1)
ac = Dungeon("Ascalonian Catacombs", [ac_s, ac_1, ac_2, ac_3])

cm_s = Path("Story",       0, 1)
cm_1 = Path("Asura",       1, 1)
cm_2 = Path("Seraph",      2, 2)
cm_3 = Path("Butler",      3, 2)
cm = Dungeon("Caudecus Manor", [cm_s, cm_1, cm_2, cm_3])

ta_s = Path("Story",       0, 1)
ta_1 = Path("Leurent",     1, 1)
ta_2 = Path("Vevina",      2, 1)
ta_3 = Path("Aetherpath",  3, 3)
ta = Dungeon("Twilight Arbor", [ta_s, ta_1, ta_2, ta_3])

se_s = Path("Story",       0, 1)
se_1 = Path("Fergg",       1, 1)
se_2 = Path("Rasolov",     2, 2)
se_3 = Path("Koptev",      3, 1)
se = Dungeon("Sorrow's Embrace", [se_s, se_1, se_2, se_3])

hotw_s = Path("Story",     0, 2)
hotw_1 = Path("Butcher",   1, 1)
hotw_2 = Path("Plunderer", 2, 2)
hotw_3 = Path("Zealot",    3, 2)
hotw = Dungeon("Honor of the Waves", [hotw_s, hotw_1, hotw_2, hotw_3])

coe_s = Path("Story",      0, 1)
coe_1 = Path("Submarine",  1, 1)
coe_2 = Path("Teleporter", 2, 2)
coe_3 = Path("Front Door", 3, 1)
coe = Dungeon("Crucibal of Eternity", [coe_s, coe_1, coe_2, coe_3])

cof_s = Path("Story",      0, 1)
cof_1 = Path("Ferrah",     1, 1)
cof_2 = Path("Magg",       2, 1)
cof_3 = Path("Rhiannon",   3, 2)
cof = Dungeon("Citadel of Flame", [cof_s, cof_1, cof_2, cof_3])

arah_s = Path("Story",     0, 3)
arah_1 = Path("Jotun",     1, 3)
arah_2 = Path("Mursaat",   2, 3)
arah_3 = Path("Forgotten", 3, 3)
arah_4 = Path("Seer",      4, 3)
arah = Dungeon("Ruined City of Arah", [arah_s, arah_1, arah_2, arah_3, arah_4])

dungeons = [ac, cm, ta, se, hotw, coe, cof, arah]
forbidden_paths = [arah_s]

# Pick a random dungeon, pick a random path, check its difficulty and if valid add it to paths
# paths is a list of DungeonPaths of the given difficulty
def gen_paths(quantity, difficulty):
    paths = []
    dungeonpaths = []
    while len(paths) < quantity:
        dungeon = dungeons[randint(0, len(dungeons))-1]
        path = dungeon.paths[randint(0, len(dungeon.paths))-1]
        if path not in paths and path not in forbidden_paths and path.difficulty == difficulty:
            paths.append(path)
            dungeonpaths.append(DungeonPath(dungeon, path))
    return dungeonpaths

# Iterate over list of dungeonpaths and print them
def print_dungeonpaths(dungeonpaths):
 for dungeonpath in dungeonpaths:
    print("    {}".format(dungeonpath.str()))


def print_discord_message(easy_paths, medium_paths, hard_paths):
    today = datetime.date.today()
    next_friday = today + datetime.timedelta((4-today.weekday()) % 7)
    print("**— Guild Dungeons {} —**".format(next_friday))
    print("*Gather in the Guild Hall to form groups at 20:00 CET/CEST*")
    print()
    if len(easy_paths) > 0:
        print("Easy dungeon{}:".format("" if len(easy_paths) == 1 else "s"))
        print_dungeonpaths(easy_paths)
        print()
    if len(medium_paths) > 0:
        print("Medium dungeon{}:".format("" if len(medium_paths) == 1 else "s"))
        print_dungeonpaths(medium_paths)
        print()
    if len(hard_paths) > 0:
        print("Hard dungeon{}:".format("" if len(hard_paths) == 1 else "s"))
        print_dungeonpaths(hard_paths)

def count_paths(dungeons):
    # 1 = easy, 2 = medium, 3 = hard
    path_totals = {1 : 0, 2: 0, 3:  0}
    for dungeon in dungeons:
        for path in dungeon.paths:
            if path not in forbidden_paths:
                path_totals[path.difficulty]+=1
    return path_totals

def main():
    seed()
    path_totals = count_paths(dungeons)

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--easy", type=int, choices=range(0, path_totals[1]), default=default_easy_paths, help="number of easy paths to roll (default {})".format(default_easy_paths))
    parser.add_argument("-m", "--medium", type=int, choices=range(0, path_totals[2]), default=default_easy_paths, help="number of medium paths to roll (default {})".format(default_medium_paths))
    parser.add_argument("-H", "--hard", type=int, choices=range(0, path_totals[3]), default=default_easy_paths, help="number of hard paths to roll (default {})".format(default_hard_paths))

    args = parser.parse_args()

    easy_paths = gen_paths(args.easy, 1)
    medium_paths = gen_paths(args.medium, 2)
    hard_paths = gen_paths(args.hard, 3)

    print_discord_message(easy_paths, medium_paths, hard_paths)

if __name__ == "__main__":
    main()
