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
        mcstats.StatDiffReader(
            mcstats.StatReader(['minecraft:used','minecraft:torch']),
            mcstats.StatReader(['minecraft:mined','minecraft:torch']))
    ))
