from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'give_diamond',
        {
            'title': 'Welfare',
            'desc': 'Diamonds given away',
            'unit': 'int',
        },
        # subtract dropped from picked up
        mcstats.StatDiffReader(
            mcstats.StatReader(['minecraft:dropped','minecraft:diamond']),
            mcstats.StatReader(['minecraft:picked_up','minecraft:diamond']))
    ))
