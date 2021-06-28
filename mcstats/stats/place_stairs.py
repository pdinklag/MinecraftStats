from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_stairs',
        {
            'unit': 'int',
        },
        # subtract mined from placed
        mcstats.StatSumMatchReader(['minecraft:used'],['minecraft:.+_stairs'])
    ))
