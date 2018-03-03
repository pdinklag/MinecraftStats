from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'jump',
        {
            'title': 'Bunnyhopper',
            'desc': 'Times jumped',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:fall_one_cm'])
    ))
