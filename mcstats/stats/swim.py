from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'swim',
        {
            'title': 'Swimmer',
            'desc': 'Distance swum',
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:swim_one_cm'])
    ))
