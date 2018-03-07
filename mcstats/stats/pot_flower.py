from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'pot_flower',
        {
            'title': 'Florist',
            'desc': 'Flowers potted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:pot_flower'])
    ))
