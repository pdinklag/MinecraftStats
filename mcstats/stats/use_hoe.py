from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_hoe',
        {
            'title': 'Farmer',
            'desc': 'Ground blocks plowed',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:.+_hoe'])
    ))
