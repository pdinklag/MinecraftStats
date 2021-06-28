from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_bars',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:used','minecraft:iron_bars']),
            mcstats.StatReader(['minecraft:used','minecraft:chain']),
        ])
    ))
