from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_tall_grass',
        {
            'title': 'Lawnmower',
            'desc': 'Tall grass removed',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:mined','minecraft:tall_grass'])
    ))
