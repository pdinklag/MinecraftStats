from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftCustomStat(
        'traveler',
        {
            'name': 'Traveler',
            'desc': 'Distance walked',
            'icon': 'items/iron_boots.png',
            'unit': 'cm',
        },
        'minecraft:walk_one_cm'))
