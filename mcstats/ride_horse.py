from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'ride_horse',
        {
            'title': 'Rider',
            'desc': 'Distance ridden on a horse',
            'unit': 'cm',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:horse_one_cm'])
    ))
