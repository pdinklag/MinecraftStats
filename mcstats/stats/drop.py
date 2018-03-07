from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'drop',
        {
            'title': 'Dropper',
            'desc': 'Items dropped',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:drop'])
    ))
