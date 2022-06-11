from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_goat_horn',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:goat_horn']),
        3093 # added in 22w17a
    ))
