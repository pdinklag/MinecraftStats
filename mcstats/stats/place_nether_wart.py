from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_nether_wart',
        {
            'title': 'Nether Farmer',
            'desc': 'Nether warts planted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:nether_wart'])
    ))
