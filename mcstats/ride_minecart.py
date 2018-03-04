from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'ride_minecart',
        {
            'title': 'Public Transport',
            'desc': 'Distance gone in a minecart',
            'unit': 'cm',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:minecart_one_cm'])
    ))
