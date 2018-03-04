from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'eat_cookie',
        {
            'title': 'Cookie Monster',
            'desc': 'Cookies eaten',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:cookie'])
    ))
