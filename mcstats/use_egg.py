from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_egg',
        {
            'title': 'Catch!',
            'desc': 'Eggs thrown',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:egg'])
    ))
