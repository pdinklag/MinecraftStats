from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_candle',
        {
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:.*candle']),
        2681 # lanterns added in 20w45a
    ))
