from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_kelp',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:mined','minecraft:kelp']),
            mcstats.StatReader(['minecraft:mined','minecraft:kelp_plant']),
        ]),
        1467 # kelp added in 18w07a
    ))
