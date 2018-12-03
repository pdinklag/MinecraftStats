from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_crossbow',
        {
            'title': 'Sharpshooter',
            'desc': 'Bolts fired',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:crossbow'])
    ))
