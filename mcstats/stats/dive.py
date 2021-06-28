from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'dive',
        {
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:walk_under_water_one_cm'])
    ))
