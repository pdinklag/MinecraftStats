from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_cactus',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:cactus'])
    ))
