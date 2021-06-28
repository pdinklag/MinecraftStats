from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_banner',
        {
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:.*banner'])
    ))
