from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'aviate',
        {
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:aviate_one_cm'])
    ))
