from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_clock',
        {
            'title': 'Timekeeper',
            'desc': 'Clocks crafted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:clock']),
    ))
