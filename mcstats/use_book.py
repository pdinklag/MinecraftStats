from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_book',
        {
            'title': 'Bestseller',
            'desc': 'Books written',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:writable_book'])
    ))
