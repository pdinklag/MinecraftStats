from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'breed',
        {
            'title': 'Ranch',
            'desc': 'Animals bred',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:animals_bred'])
    ))
