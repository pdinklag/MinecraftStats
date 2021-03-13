from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'interact_lectern',
        {
            'title': 'Lector',
            'desc': 'Lectern interactions',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:interact_with_lectern']),
        1921 # lecterns usable since 19w02a
    ))
