from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'climb',
        {
            'title': 'Climber',
            'desc': 'Distance climbed',
            'unit': 'cm',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:climb_one_cm'])
    ))
