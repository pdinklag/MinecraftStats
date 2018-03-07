from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'eat_cookie',
        {
            'title': 'Cookie Monster',
            'desc': 'Cookies eaten',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:cookie'])
    ))
