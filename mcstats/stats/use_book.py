from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_book',
        {
            'title': 'Bestseller',
            'desc': 'Books written',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:writable_book'])
    ))
