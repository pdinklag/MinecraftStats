from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_grass',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:mined','minecraft:grass']),
            mcstats.StatReader(['minecraft:mined','minecraft:tall_grass']),
        ])
    ))
