from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_bars',
        {
            'title': 'Jailer',
            'desc': 'Iron bars placed',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:iron_bars'])
    ))
