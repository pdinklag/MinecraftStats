from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_clock',
        {
            'title': 'Timekeeper',
            'desc': 'Clocks crafted',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:crafted','minecraft:clock']),
    ))
