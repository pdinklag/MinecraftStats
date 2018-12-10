from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_nether_wart',
        {
            'title': 'Nether Farmer',
            'desc': 'Nether warts harvested',
            'unit': 'int',
        },
        mcstats.StatDiffReader(
            mcstats.StatReader(['minecraft:picked_up','minecraft:nether_wart']),
            mcstats.StatReader(['minecraft:used','minecraft:nether_wart'])
        )
    ))
