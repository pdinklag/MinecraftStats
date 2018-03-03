from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'fall',
        {
            'title': 'Base Jumper',
            'desc': 'Distance fallen',
            'unit': 'cm',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:fall_one_cm'])
    ))
