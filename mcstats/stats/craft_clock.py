from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_clock',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:clock']),
    ))
