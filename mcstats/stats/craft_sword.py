from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_sword',
        {
            'title': 'Blacksmith',
            'desc': 'Swords crafted',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:crafted'],
            ['minecraft:.+_sword'])
    ))
