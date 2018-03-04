from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_ender_pearl',
        {
            'title': 'Translocator',
            'desc': 'Ender pearls thrown',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:ender_pearl'])
    ))
