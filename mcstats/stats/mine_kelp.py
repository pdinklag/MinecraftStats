from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_kelp',
        {
            'title': 'I Need Kelp!',
            'desc': 'Kelp mined',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:mined','minecraft:kelp']),
            mcstats.StatReader(['minecraft:mined','minecraft:kelp_plant']),
        ]),
        1467 # kelp added in 18w07a
    ))
