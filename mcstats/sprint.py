from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'sprint',
        {
            'title': 'Marathon',
            'desc': 'Distance sprinted',
            'unit': 'cm',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:sprint_one_cm'])
    ))
