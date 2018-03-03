from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'dive',
        {
            'title': 'Diver',
            'desc': 'Distance dived',
            'unit': 'cm',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:dive_one_cm'])
    ))
