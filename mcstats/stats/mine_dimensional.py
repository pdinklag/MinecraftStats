from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_dimensional',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:mined','minecraft:end_stone']),
            mcstats.StatReader(['minecraft:mined','minecraft:netherrack'])
        ])
    ))
