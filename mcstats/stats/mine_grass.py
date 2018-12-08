from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_tall_grass',
        {
            'title': 'Lawnmower',
            'desc': 'Grass removed',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:mined','minecraft:grass']),
            mcstats.StatReader(['minecraft:mined','minecraft:tall_grass']),
        ])
    ))
