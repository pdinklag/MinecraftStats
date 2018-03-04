from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'place_piston',
        {
            'title': 'Mechanic',
            'desc': 'Pistons placed',
            'unit': 'int',
        },
        __mcstats__.StatDiffReader(
            __mcstats__.StatSumMatchReader(
                ['minecraft:used'],
                ['minecraft:.*piston']),
            __mcstats__.StatSumMatchReader(
                ['minecraft:mined'],
                ['minecraft:.*piston'])),
    ))
