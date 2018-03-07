from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_egg',
        {
            'title': 'Catch!',
            'desc': 'Eggs thrown',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:egg'])
    ))
