from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_ice',
        {
            'title': 'Ice Breaker',
            'desc': 'Ice broken',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:mined','minecraft:ice']),
            mcstats.StatReader(['minecraft:mined','minecraft:packed_ice']),
        ])
    ))
