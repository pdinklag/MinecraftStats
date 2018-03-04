from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'place_conveyor',
        {
            'title': 'Conveyor',
            'desc': 'Hoppers and droppers placed',
            'unit': 'int',
        },
        __mcstats__.StatDiffReader(
            __mcstats__.StatSumMatchReader(
                ['minecraft:used'],
                ['minecraft:hopper','minecraft:dropper']),
            __mcstats__.StatSumMatchReader(
                ['minecraft:mined'],
                ['minecraft:hopper','minecraft:dropper']),
        )
    ))
