from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'fall',
        {
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:fall_one_cm'])
    ))
