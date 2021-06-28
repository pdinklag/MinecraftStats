from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'breed',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:animals_bred'])
    ))
