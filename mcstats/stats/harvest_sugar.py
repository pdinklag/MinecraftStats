from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'harvest_sugar',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:picked_up','minecraft:sugar_cane']),
    ))
