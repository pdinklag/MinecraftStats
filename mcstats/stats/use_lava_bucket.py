from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_lava_bucket',
        {
            'title': 'Napalm',
            'desc': 'Lava buckets emptied',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:lava_bucket'])
    ))
