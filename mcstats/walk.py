from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'walk',
        {
            'title': 'Traveler',
            'desc': 'Distance walked',
            'unit': 'cm',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:walk_one_cm'])
    ))
