from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_coral',
        {
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:mined'],[
                'minecraft:.+_coral',
                'minecraft:.+_coral_block',
                'minecraft:.+_coral_fan',
                'minecraft:.+_coral_wall_fan',
            ]
        ),
        1473 # corals added in 18w10a
    ))
