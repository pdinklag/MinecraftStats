from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_wool',
        {
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:crafted'],
            [
                'minecraft:.+_wool',
                'minecraft:.+_carpet'
            ])
    ))
