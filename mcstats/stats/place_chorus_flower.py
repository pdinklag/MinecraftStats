from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_chorus_flower',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:chorus_flower'])
    ))
