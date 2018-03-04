from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'place_banner',
        {
            'title': 'Propaganda',
            'desc': 'Banners placed',
            'unit': 'int',
        },
        # subtract mined from placed
        __mcstats__.StatDiffReader(
            __mcstats__.StatSumMatchReader(
                ['minecraft:used'],
                ['minecraft:.*banner']),
            __mcstats__.StatSumMatchReader(
                ['minecraft:mined'],
                ['minecraft:.*sapling'])),
    ))
