from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'fall',
        {
            'title': 'Base Jumper',
            'desc': 'Distance fallen',
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:fall_one_cm'])
    ))
