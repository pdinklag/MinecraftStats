from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_tools',
        {
            'title': 'Workshop',
            'desc': 'Tools crafted',
            'unit': 'int',
        },
        __mcstats__.StatSumMatchReader(
            ['minecraft:crafted'],
            [
                'minecraft:.+_axe',
                'minecraft:.+_hoe',
                'minecraft:.+_pickaxe',
                'minecraft:.+_shovel',
                'minecraft:fishing_rod',
                'minecraft:flint_and_steel',
                'minecraft:shears',
            ])
    ))
