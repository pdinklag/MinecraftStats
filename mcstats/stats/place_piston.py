from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_piston',
        {
            'title': 'Mechanic',
            'desc': 'Pistons placed',
            'unit': 'int',
        },
        mcstats.StatDiffReader(
            mcstats.StatSumMatchReader(
                ['minecraft:used'],
                ['minecraft:.*piston']),
            mcstats.StatSumMatchReader(
                ['minecraft:mined'],
                ['minecraft:.*piston'])),
    ))
