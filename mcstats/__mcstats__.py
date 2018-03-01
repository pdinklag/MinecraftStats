import json

# reads a statistic from the given stats object
# stats   -- the player stats object
# path    -- the JSON path to the desired value
# default -- the default value
def read(stats, path, default):
    for key in path:
        if key in stats:
            stats = stats[key]
        else:
            return default

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
    def __init__(self, name):
        Ranking.__init__(self)
        self.name = name

    # read the statistic value from the player stats
    def read(self, stats):
        raise Exception('not implemented')

# Base for simple single-value stats
class MinecraftBasicStat(MinecraftStat):
    def __init__(self, name, path, default = 0):
        MinecraftStat.__init__(self, name)
        self.path = path
        self.default = default

    def read(self, stats):
        return read(stats, self.path, self.default)

# Statistics under 'minecraft:broken'
class MinecraftBrokenStat(MinecraftBasicStat):
    def __init__(self, name, id, default = 0):
        MinecraftBasicStat.__init__(
            self, name, ['minecraft:broken', id], default)

# Statistics under 'minecraft:crafted'
class MinecraftCraftedStat(MinecraftBasicStat):
    def __init__(self, name, id, default = 0):
        MinecraftBasicStat.__init__(
            self, name, ['minecraft:crafted', id], default)

# Statistics under 'minecraft:custom'
class MinecraftCustomStat(MinecraftBasicStat):
    def __init__(self, name, id, default = 0):
        MinecraftBasicStat.__init__(
            self, name, ['minecraft:custom', id], default)

# Statistics under 'minecraft:dropped'
class MinecraftDroppedStat(MinecraftBasicStat):
    def __init__(self, name, id, default = 0):
        MinecraftBasicStat.__init__(
            self, name, ['minecraft:dropped', id], default)

# Statistics under 'minecraft:killed'
class MinecraftKilledByStat(MinecraftBasicStat):
    def __init__(self, name, id, default = 0):
        MinecraftBasicStat.__init__(
            self, name, ['minecraft:killed', id], default)

# Statistics under 'minecraft:killed_by'
class MinecraftKilledByStat(MinecraftBasicStat):
    def __init__(self, name, id, default = 0):
        MinecraftBasicStat.__init__(
            self, name, ['minecraft:killed_by', id], default)

# Statistics under 'minecraft:mined'
class MinecraftMinedStat(MinecraftBasicStat):
    def __init__(self, name, id, default = 0):
        MinecraftBasicStat.__init__(
            self, name, ['minecraft:mined', id], default)

# Statistics under 'minecraft:picked_up'
class MinecraftPickedUpStat(MinecraftBasicStat):
    def __init__(self, name, id, default = 0):
        MinecraftBasicStat.__init__(
            self, name, ['minecraft:picked_up', id], default)

# Statistics under 'minecraft:used'
class MinecraftUsedStat(MinecraftBasicStat):
    def __init__(self, name, id, default = 0):
        MinecraftBasicStat.__init__(
            self, name, ['minecraft:used', id], default)


# the global registry
registry = []
