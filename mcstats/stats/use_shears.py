from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_shears',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:shears'])
    ))
