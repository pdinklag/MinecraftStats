from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_snowball',
        {
            'title': 'Snowball Fight!',
            'desc': 'Snowballs thrown',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:snowball'])
    ))
