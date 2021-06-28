from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_piston',
        {
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:.*piston'])
    ))
