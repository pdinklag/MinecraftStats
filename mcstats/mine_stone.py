from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'mine_stone',
        {
            'title': 'Stonemason',
            'desc': 'Stone mined',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:mined','minecraft:stone']),
            __mcstats__.StatReader(['minecraft:mined','minecraft:diorite']),
            __mcstats__.StatReader(['minecraft:mined','minecraft:andesite']),
            __mcstats__.StatReader(['minecraft:mined','minecraft:granite']),
        ])
    ))
