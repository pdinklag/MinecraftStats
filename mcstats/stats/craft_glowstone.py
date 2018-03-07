from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_glowstone',
        {
            'title': 'Illuminator',
            'desc': 'Glowstone crafted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:glowstone']),
    ))
