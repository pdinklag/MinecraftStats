from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'harvest_nether_wart',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:picked_up','minecraft:nether_wart']),
    ))
