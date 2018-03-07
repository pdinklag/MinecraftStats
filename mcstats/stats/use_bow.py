from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_bow',
        {
            'title': 'Archer',
            'desc': 'Arrows shot',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:bow'])
    ))
