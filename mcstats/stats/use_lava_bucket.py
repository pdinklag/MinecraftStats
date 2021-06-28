from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_lava_bucket',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:lava_bucket'])
    ))
