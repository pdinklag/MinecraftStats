from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_water_bucket',
        {
            'title': 'Aqueduct',
            'desc': 'Water buckets emptied',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:water_bucket'])
    ))
