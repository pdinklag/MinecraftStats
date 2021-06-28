from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'sprint',
        {
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:sprint_one_cm'])
    ))
