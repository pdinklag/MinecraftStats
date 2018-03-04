from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_dirt',
        {
            'title': 'Dirtbag',
            'desc': 'Dirt blocks placed',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:dirt'])
    ))
