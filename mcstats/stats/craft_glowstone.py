from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_glowstone',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:glowstone']),
    ))
