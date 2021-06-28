from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'death',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:deaths'])
    ))
