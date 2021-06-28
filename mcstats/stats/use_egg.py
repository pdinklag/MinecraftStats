from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_egg',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:egg'])
    ))
