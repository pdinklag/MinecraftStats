from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'break_tools',
        {
            'title': 'Oh snap',
            'desc': 'Tools broken',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
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
