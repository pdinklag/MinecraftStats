from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_piston',
        {
            'title': 'Mechanic',
            'desc': 'Pistons placed',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:.*piston'])
    ))
