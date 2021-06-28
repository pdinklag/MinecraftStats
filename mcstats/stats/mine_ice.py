from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_ice',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:mined','minecraft:ice']),
            mcstats.StatReader(['minecraft:mined','minecraft:packed_ice']),
            mcstats.StatReader(['minecraft:mined','minecraft:blue_ice']),
            mcstats.StatReader(['minecraft:mined','minecraft:frosted_ice']),
        ])
    ))
