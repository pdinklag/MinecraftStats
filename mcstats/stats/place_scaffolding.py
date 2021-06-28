from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_scaffolding',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:scaffolding']),
        1908 # scaffolding added in 18w45a
    ))
