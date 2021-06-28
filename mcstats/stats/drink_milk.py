from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'drink_milk',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:milk_bucket'])
    ))
