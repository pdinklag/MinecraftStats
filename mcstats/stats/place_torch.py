from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_torch',
        {
            'title': 'Enlightened',
            'desc': 'Torches placed',
            'unit': 'int',
        },
        # subtract mined from placed
        mcstats.StatSumReader([
            mcstats.StatDiffReader(
                mcstats.StatReader(['minecraft:used','minecraft:torch']),
                mcstats.StatReader(['minecraft:mined','minecraft:torch']),
            ),
            mcstats.StatDiffReader(
                mcstats.StatReader(['minecraft:used','minecraft:soul_torch']),
                mcstats.StatReader(['minecraft:mined','minecraft:soul_torch']),
            ),
        ]),
    ))
