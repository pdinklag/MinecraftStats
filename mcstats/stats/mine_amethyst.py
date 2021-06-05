from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_amethyst',
        {
            'title': 'Jeweler',
            'desc': 'Amethysts mined',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:mined'],[
                'minecraft:.+_amethyst_bud',
                'minecraft:amethyst_cluster',
            ]
        ),
        2681 # added in 20w45a
    ))
