from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_flint',
        {
            'title': 'Pyromaniac',
            'desc': 'Fires started',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:flint_and_steel'])
    ))
