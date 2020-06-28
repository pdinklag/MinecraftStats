from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_bars',
        {
            'title': 'Jailer',
            'desc': 'Iron bars & chains placed',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:used','minecraft:iron_bars']),
            mcstats.StatReader(['minecraft:used','minecraft:chain']),
        ])
    ))
