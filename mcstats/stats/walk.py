from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'walk',
        {
            'title': 'Traveler',
            'desc': 'Distance walked',
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:walk_one_cm'])
    ))
