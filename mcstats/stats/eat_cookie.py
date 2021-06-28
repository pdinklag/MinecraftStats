from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'eat_cookie',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:cookie'])
    ))
