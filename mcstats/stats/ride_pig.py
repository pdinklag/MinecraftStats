from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'ride_pig',
        {
            'title': 'Because I Can!',
            'desc': 'Distance ridden on a pig',
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:pig_one_cm'])
    ))
