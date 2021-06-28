from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'drop',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:drop'])
    ))
