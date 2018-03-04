from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'place_glass',
        {
            'title': 'Glassworker',
            'desc': 'Glass placed',
            'unit': 'int',
        },
        # subtract mined from placed
        __mcstats__.StatDiffReader(
            __mcstats__.StatSumMatchReader(
                ['minecraft:used'],
                ['minecraft:glass','minecraft:.*glass_pane']),
            __mcstats__.StatSumMatchReader(
                ['minecraft:mined'],
                ['minecraft:glass','minecraft:.*glass_pane']))
    ))
