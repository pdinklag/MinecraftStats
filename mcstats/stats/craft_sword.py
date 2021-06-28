from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_sword',
        {
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:crafted'],
            ['minecraft:.+_sword'])
    ))
