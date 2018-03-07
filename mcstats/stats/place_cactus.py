from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_cactus',
        {
            'title': 'Cactus Farmer',
            'desc': 'Cacti planted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:cactus'])
    ))
