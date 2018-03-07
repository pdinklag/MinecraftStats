import json
import re

# basic path reading function
def read(stats, path, default):
    for key in path:
        if key in stats:
            stats = stats[key]
        else:
            return default

    return stats

# Reader for a single statistic
class StatReader:
    def __init__(self, path, default = 0):
        self.path = path
        self.default = default

    # read from stats
    def read(self, stats):
        return read(stats, self.path, self.default)

# Reader that subtracts one stat from another (a minus b)
class StatDiffReader:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def read(self, stats):
        return self.a.read(stats) - self.b.read(stats)

# Reader that cumulates multiple stats
class StatSumReader:
    def __init__(self, summands):
        self.summands = summands

    def read(self, stats):
        sum = 0
        for s in self.summands:
            sum += s.read(stats)

        return sum

# Reader that sums up all stats matching one of multiple regular expressions
class StatSumMatchReader:
    def __init__(self, path, patterns):
        self.path = path
        self.progs = []
        for p in patterns:
            self.progs.append(re.compile(p))

    def read(self, stats):
        sum = 0
        group = read(stats, self.path, dict())
        for k,v in group.items():
            for p in self.progs:
                if p.match(k):
                    sum += v

        return sum

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

    # enter the player with id and value into the ranking
    def enter(self, id, value):
        # only if greater than zero
        if value > 0:
            Ranking.enter(self, id, value)

    # read the statistic value from the player stats
    def read(self, stats):
        return self.reader.read(stats)

# Crown score (a meta statistic)
class CrownScore:
    def __init__(self):
        self.score = [0,0,0,0]

    def increase(self, i):
        self.score[i+1] += 1
        self.score[0] = 4*self.score[1] + 2*self.score[2] + self.score[3]

class CrownScoreRanking(Ranking):
    def sort(self):
        self.ranking = sorted(
            self.ranking, key = lambda x : x[1].score[0], reverse = True)

# the global registry
registry = []
