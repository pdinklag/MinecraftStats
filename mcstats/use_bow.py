from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_bow',
        {
            'title': 'Archer',
            'desc': 'Arrows shot',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:bow'])
    ))
