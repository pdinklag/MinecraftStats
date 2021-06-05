from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_conveyor',
        {
            'title': 'Conveyor',
            'desc': 'Hoppers and droppers placed',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:hopper','minecraft:dropper'])
    ))
