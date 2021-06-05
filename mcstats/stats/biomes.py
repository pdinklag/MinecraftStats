from mcstats import mcstats

# Reader that reads a list
class StatListReader:
    def __init__(self, path):
        self.path = path

    # read from stats
    def read(self, stats):
        return mcstats.read(stats, self.path, [])

# aggregate two sets
def aggregateExplorer(a, b):
    merged = a['biomes']
    merged.update(b['biomes'])
    return { 'biomes': merged, 'value': len(merged) }

# special stat class for Explorer award
class ExplorerStat(mcstats.MinecraftStat):
    def __init__(self, name, meta, reader, minVersion = 1451, maxVersion = float("inf")):
        mcstats.MinecraftStat.__init__(self, name, meta, reader, minVersion, maxVersion)
        self.aggregate = aggregateExplorer

    def read(self, stats):
        biomes = set()
        biomes.update(self.reader.read(stats))
        return { 'biomes': biomes, 'value': len(biomes) } 

mcstats.registry.append(
    ExplorerStat(
        'biomes',
        {
            'title': 'Explorer',
            'desc': 'Biomes discovered',
            'unit': 'int',
        },
        StatListReader([
            'advancements',
            'minecraft:adventure/adventuring_time',
            'criteria'
        ])
    ))
