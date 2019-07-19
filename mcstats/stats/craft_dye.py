from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_dye',
        {
            'title': 'Chemist',
            'desc': 'Dyes crafted',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:crafted'],
            ['minecraft:.*_dye'])
    ))
