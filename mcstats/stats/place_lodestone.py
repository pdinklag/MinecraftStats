from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_lodestone',
        {
            'title': 'Lodecrumb Trail',
            'desc': 'Lodestone placed',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:lodestone']),
        2520 # added in 20w13a
    ))
