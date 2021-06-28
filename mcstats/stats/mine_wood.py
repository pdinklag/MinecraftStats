from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_wood',
        {
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:mined'],['minecraft:.+_log', 'minecraft:.+_stem'])
    ))
