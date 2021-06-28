from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_book',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:writable_book'])
    ))
