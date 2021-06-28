from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'ride_boat',
        {
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:boat_one_cm'])
    ))
