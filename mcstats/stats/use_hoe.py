from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_hoe',
        {
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:.+_hoe'])
    ))
