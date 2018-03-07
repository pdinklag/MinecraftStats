from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_rails',
        {
            'title': 'Railway Company',
            'desc': 'Rails placed',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:.*rail'])
    ))
