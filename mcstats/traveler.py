from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'traveler',
        {
            'name': 'Traveler',
            'desc': 'Distance walked',
            'icon': 'items/iron_boots.png',
            'unit': 'cm',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:walk_one_cm'])
    ))
