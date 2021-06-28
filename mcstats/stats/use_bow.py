from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_bow',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:bow'])
    ))
