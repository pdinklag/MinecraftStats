from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_ender_pearl',
        {
            'title': 'Translocator',
            'desc': 'Ender pearls thrown',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:ender_pearl'])
    ))
