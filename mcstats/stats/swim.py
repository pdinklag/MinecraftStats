from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'swim',
        {
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:swim_one_cm'])
    ))
