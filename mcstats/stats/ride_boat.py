from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'ride_boat',
        {
            'title': 'Sailor',
            'desc': 'Distance gone by boat',
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:boat_one_cm'])
    ))
