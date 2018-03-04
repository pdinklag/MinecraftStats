from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'mine_ice',
        {
            'title': 'Ice Breaker',
            'desc': 'Ice broken',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:mined','minecraft:ice']),
            __mcstats__.StatReader(['minecraft:mined','minecraft:packed_ice']),
        ])
    ))
