from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'ride_pig',
        {
            'title': 'Because I Can!',
            'desc': 'Distance ridden on a pig',
            'unit': 'cm',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:pig_one_cm'])
    ))
