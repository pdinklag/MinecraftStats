from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_torch',
        {
            'unit': 'int',
        },
        # subtract mined from placed
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:used','minecraft:torch']),
            mcstats.StatReader(['minecraft:used','minecraft:soul_torch']),
        ])
    ))
