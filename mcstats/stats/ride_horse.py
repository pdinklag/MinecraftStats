from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'ride_horse',
        {
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:horse_one_cm'])
    ))
