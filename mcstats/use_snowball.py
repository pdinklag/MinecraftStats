from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_snowball',
        {
            'title': 'Snowball Fight!',
            'desc': 'Snowballs thrown',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:snowball'])
    ))
