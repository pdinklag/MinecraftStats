from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_ender_eye',
        {
            'title': 'Stronghold Seeker',
            'desc': 'Ender eyes thrown',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:ender_eye'])
    ))
