from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'drink_milk',
        {
            'title': 'Milksop',
            'desc': 'Milk buckets drunk',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:milk_bucket'])
    ))
