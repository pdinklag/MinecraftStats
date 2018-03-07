from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_wool',
        {
            'title': 'Clothier',
            'desc': 'Wool crafted or dyed',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:crafted'],
            ['minecraft:.+_wool'])
    ))
