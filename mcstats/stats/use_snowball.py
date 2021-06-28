from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_snowball',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:snowball'])
    ))
