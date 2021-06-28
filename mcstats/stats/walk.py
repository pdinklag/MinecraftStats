from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'walk',
        {
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:walk_one_cm'])
    ))
