from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_flint',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:flint_and_steel'])
    ))
