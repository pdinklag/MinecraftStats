import json
import re
import time

# get a fixed sense of "now"
now = int(time.time())

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
            self.progs.append(re.compile('^{}$'.format(p)))

    def read(self, stats):
        sum = 0
        group = read(stats, self.path, dict())
        for k,v in group.items():
            for p in self.progs:
                if p.match(k):
                    sum += v

        return sum

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

# Aggregation functions
def aggregateSum(a, b):
    return {'value': a['value'] + b['value']}

# Base for all minecraft stats
class MinecraftStat(Ranking):
    def __init__(self, name, meta, reader, minVersion = 1451, maxVersion = float("inf")):
        Ranking.__init__(self)
        self.name = name
        self.meta = meta
        self.reader = reader
        self.minVersion = max(minVersion, 1451) # 1451 = 17w47a is the absolute minimum
        self.maxVersion = maxVersion
        self.linkedStat = False
        self.playerStatRelevant = True
        self.aggregate = aggregateSum

    # enter the player with id and value into the ranking
    def enter(self, id, value):
        # only if greater than zero
        if value > 0:
            Ranking.enter(self, id, value)
        #elif value < 0:
        #    print('Negative value (' + str(value) + ') for stat ' + self.name)

    # read the statistic value from the player stats
    def read(self, stats):
        return {'value': self.reader.read(stats)}

    # test if this stat can be used right now
    def isEligible(self, version):
        return (version >= self.minVersion and version <= self.maxVersion)

    # test if this player may enter the ranking
    def canEnterRanking(self, id, active):
        return active

# Legacy statistics for supporting older data versions
class LegacyStat:
    def __init__(self, link, minVersion, maxVersion, reader):
        self.link = link
        self.name = link.name
        self.minVersion = minVersion
        self.maxVersion = maxVersion
        self.reader = reader
        self.linkedStat = True
        self.playerStatRelevant = True

    # enter the player with id and value into the linked ranking
    def enter(self, id, value):
        self.link.enter(id, value)

    # read the statistic value from the player stats
    def read(self, stats):
        return {'value': self.reader.read(stats)}

    # test if this stat can be used right now
    def isEligible(self, version):
        return MinecraftStat.isEligible(self, version);

    # test if this player may enter the ranking
    def canEnterRanking(self, id, active):
        return active

# Event statistics for temporary events
# similar to event stats in some ways
class EventStat(Ranking):
    def __init__(self, name, title, link, startTime = None, stopTime = None, initialRanking = dict(), ranking = [], active = True):
        global now

        self.name = name
        self.title = title
        self.link = link
        self.minVersion = link.minVersion
        self.maxVersion = link.maxVersion
        self.startTime = now if startTime is None else startTime
        self.stopTime = stopTime
        self.initialRanking = initialRanking
        self.ranking = ranking
        self.active = active
        self.linkedStat = True
        self.playerStatRelevant = False

    # enter the player with id and value delta into the ranking
    def enter(self, id, value):
        global now

        if now > self.startTime:
            # subtract initial value and enter
            if id in self.initialRanking:
                initial = self.initialRanking[id]
            else:
                initial = 0

            MinecraftStat.enter(self, id, value - initial)
        elif value > 0:
            # first time we are entering somebody
            # do not really enter, but only save the initial score
            self.initialRanking[id] = value

    # read the statistic value from the player stats via the linked stat
    def read(self, stats):
        return {'value': self.link.read(stats)}

    # test if this stat can be used right now
    def isEligible(self, version):
        return MinecraftStat.isEligible(self, version) if self.active else False

    # test if this player may enter the ranking
    def canEnterRanking(self, id, active):
        global now
        return active if now > self.startTime else True # enter everybody into the initial ranking

    # serializes the event stat to a dictionary
    def serialize(self):
        ranking = []
        for entry in self.ranking:
            ranking.append({'uuid':entry.id,'value':entry.value})

        return {
            'name':           self.name,
            'title':          self.title,
            'link':           self.link.name,
            'startTime':      self.startTime,
            'stopTime':       self.stopTime,
            'initialRanking': self.initialRanking,
            'ranking':        ranking,
            'active':         self.active
        }

    # deserializes an event stat from a dictionary
    def deserialize(data, registry):
        ranking = []
        for entry in data['ranking']:
            ranking.append(RankingEntry(entry['uuid'], entry['value']))

        return EventStat(
            data['name'],
            data['title'],
            registry[data['link']],
            data['startTime'],
            data['stopTime'],
            data['initialRanking'],
            ranking,
            data['active'])

# Crown score (a meta statistic)
class CrownScore:
    # worth of medals
    gold   = 4
    silver = 2
    bronze = 1

    def compute(g, s, b):
        return CrownScore.gold * g + CrownScore.silver * s + CrownScore.bronze * b

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
        self.score[0] = CrownScore.compute(self.score[1], self.score[2], self.score[3])

# the global registry
registry = []
