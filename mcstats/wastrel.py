from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'wastrel',
        {
            'title': 'Wastrel',
            'desc': 'Tools broken',
            'icon': 'items/stick.png',
            'unit': 'int',
        },
        __mcstats__.StatSumMatchReader(
            ['minecraft:broken'],
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
