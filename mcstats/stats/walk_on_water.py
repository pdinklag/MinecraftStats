from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'walk_on_water',
        {
            'title': 'Water Walker',
            'desc': 'Distance walked on water',
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:walk_on_water_one_cm'])
    ))
