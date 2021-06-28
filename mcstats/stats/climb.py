from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'climb',
        {
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:climb_one_cm'])
    ))
