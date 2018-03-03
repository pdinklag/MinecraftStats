from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_armor',
        {
            'title': 'Armorer',
            'desc': 'Pieces of armor crafted',
            'unit': 'int',
        },
        __mcstats__.StatSumMatchReader(
            ['minecraft:crafted'],
            [
                'minecraft:.+_helmet',
                'minecraft:.+_leggings',
                'minecraft:.+_boots',
                'minecraft:.+_chestplate',
                'minecraft:shield',
            ])
    ))
