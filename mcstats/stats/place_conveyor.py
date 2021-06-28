from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_conveyor',
        {
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:hopper','minecraft:dropper'])
    ))
