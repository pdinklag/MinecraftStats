from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_glass',
        {
            'title': 'Glassworker',
            'desc': 'Glass placed',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:glass','minecraft:.*glass_pane']),
    ))
