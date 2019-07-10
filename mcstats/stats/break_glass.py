from mcstats import mcstats
mcstats.registry.append(
    mcstats.MinecraftStat(
        'break_glass',
        {
            'title': 'Glassbreaker',
            'desc': 'Glass broken',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:mined'],
            ['minecraft:glass','minecraft:.*glass_pane','minecraft:.*stained_glass']),
    ))
