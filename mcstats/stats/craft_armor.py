from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_armor',
        {
            'title': 'Armorer',
            'desc': 'Pieces of armor crafted',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:crafted'],
            [
                'minecraft:.+_helmet',
                'minecraft:.+_leggings',
                'minecraft:.+_boots',
                'minecraft:.+_chestplate',
                'minecraft:shield',
            ])
    ))
