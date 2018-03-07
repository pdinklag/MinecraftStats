from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_glass',
        {
            'title': 'Glassworker',
            'desc': 'Glass placed',
            'unit': 'int',
        },
        # subtract mined from placed
        mcstats.StatDiffReader(
            mcstats.StatSumMatchReader(
                ['minecraft:used'],
                ['minecraft:glass','minecraft:.*glass_pane']),
            mcstats.StatSumMatchReader(
                ['minecraft:mined'],
                ['minecraft:glass','minecraft:.*glass_pane']))
    ))
