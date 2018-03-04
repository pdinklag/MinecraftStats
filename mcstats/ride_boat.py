from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'ride_boat',
        {
            'title': 'Sailor',
            'desc': 'Distance gone by boat',
            'unit': 'cm',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:boat_one_cm'])
    ))
