from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'jump',
        {
            'title': 'Bunnyhopper',
            'desc': 'Times jumped',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:fall_one_cm'])
    ))
