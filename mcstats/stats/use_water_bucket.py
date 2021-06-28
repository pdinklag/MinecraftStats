from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_water_bucket',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:water_bucket'])
    ))
