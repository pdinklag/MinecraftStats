import json

# Reader for a single statistic
class StatReader:
    def __init__(self, path, default = 0):
        self.path = path
        self.default = default

    # read from stats
    def read(self, stats):
        for key in self.path:
            if key in stats:
                stats = stats[key]
            else:
                return self.default

        return stats

# Rankings
class Ranking:
    def __init__(self):
        self.ranking = []

    # enter the player with id and value into the ranking
    def enter(self, id, value):
        self.ranking.append((id, value))

    # sort ranking and return
    def sort(self):
        # by default, sort values directly and in descending order
        self.ranking = sorted(
            self.ranking, key = lambda x : x[1], reverse = True)

# Base for all minecraft stats
class MinecraftStat(Ranking):
    def __init__(self, name, meta, reader):
        Ranking.__init__(self)
        self.name = name
        self.meta = meta
        self.reader = reader

    # read the statistic value from the player stats
    def read(self, stats):
        return self.reader.read(stats)

# the global registry
registry = []
