from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_compass',
        {
            'title': 'Navigator',
            'desc': 'Compasses crafted',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:crafted','minecraft:compass']),
    ))
