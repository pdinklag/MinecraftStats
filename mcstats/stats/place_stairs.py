from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_stairs',
        {
            'title': 'MaStair',
            'desc': 'Stairs built',
            'unit': 'int',
        },
        # subtract mined from placed
        mcstats.StatDiffReader(
            mcstats.StatSumMatchReader(
                ['minecraft:used'],
                ['minecraft:.+_stairs']),
            mcstats.StatSumMatchReader(
                ['minecraft:mined'],
                ['minecraft:.+_stairs'])),
    ))
