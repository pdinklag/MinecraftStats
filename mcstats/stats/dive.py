from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'dive',
        {
            'title': 'Diver',
            'desc': 'Distance dived',
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:dive_one_cm'])
    ))
