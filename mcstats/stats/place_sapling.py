from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_sapling',
        {
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:.+_sapling','minecraft:mangrove_propagule'])
    ))
