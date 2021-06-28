from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'ride_pig',
        {
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:pig_one_cm'])
    ))
