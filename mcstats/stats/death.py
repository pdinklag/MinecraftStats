from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'death',
        {
            'title': 'Lemming',
            'desc': 'Times died',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:deaths'])
    ))
