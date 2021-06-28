from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_crossbow',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:crossbow']),
        1901 # crossbows added in 18w43a
    ))
