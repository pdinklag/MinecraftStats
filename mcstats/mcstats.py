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

# Reader that counts the amount of entries of a list
class StatListLengthReader:
    def __init__(self, path):
        self.path = path

    # read from stats
    def read(self, stats):
        return len(read(stats, self.path, []))

# Ranking entries
class RankingEntry:
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def __eq__(self, other):
        return self.id == other.id and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.value != other.value:
            return self.value < other.value
        else: # use player ID as fallback to keep things deterministic
            return self.id < other.id

    def __gt__(self, other):
        return not self.__eq__(other) and not self.__lt__(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

# Rankings
class Ranking:
    def __init__(self):
        self.ranking = []

    # enter the player with id and value into the ranking
    def enter(self, id, value):
        self.ranking.append(RankingEntry(id, value))

    # sort ranking
    def sort(self):
        self.ranking.sort(reverse=True)

# Base for all minecraft stats
class MinecraftStat(Ranking):
    def __init__(self, name, meta, reader):
        Ranking.__init__(self)
        self.name = name
        self.meta = meta
        self.reader = reader
        self.minVersion = 1451 # 17w47a is the absolute minimum
        self.maxVersion = float("inf")

    # enter the player with id and value into the ranking
    def enter(self, id, value):
        # only if greater than zero
        if value > 0:
            Ranking.enter(self, id, value)

    # read the statistic value from the player stats
    def read(self, stats):
        return self.reader.read(stats)

# Legacy statistics for supporting older data versions
class LegacyStat:
    def __init__(self, link, minVersion, maxVersion, reader):
        self.link = link
        self.name = link.name
        self.minVersion = minVersion
        self.maxVersion = maxVersion
        self.reader = reader

    # enter the player with id and value into the linked ranking
    def enter(self, id, value):
        self.link.enter(id, value)

    # read the statistic value from the player stats
    def read(self, stats):
        return self.reader.read(stats)

# Crown score (a meta statistic)
class CrownScore:
    def __init__(self):
        self.score = [0,0,0,0]

    def __eq__(self, other):
        return self.score == other.score

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.score[0] != other.score[0]: # crown score
            return self.score[0] < other.score[0]
        elif self.score[1] != other.score[1]: # gold medals
            return self.score[1] < other.score[1]
        elif self.score[2] != other.score[2]: # silver medals
            return self.score[2] < other.score[2]
        else: # bronze medals
            return self.score[3] < other.score[3]

    def __gt__(self, other):
        return not self.__eq__(other) and not self.__lt__(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def increase(self, i):
        self.score[i+1] += 1
        self.score[0] = 4*self.score[1] + 2*self.score[2] + self.score[3]

# the global registry
registry = []
