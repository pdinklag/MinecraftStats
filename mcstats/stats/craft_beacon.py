from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_beacon',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:beacon']),
    ))
