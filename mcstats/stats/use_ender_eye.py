from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_ender_eye',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:ender_eye'])
    ))
