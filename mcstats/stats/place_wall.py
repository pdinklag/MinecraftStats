from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_wall',
        {
            'title': 'Iron Curtain',
            'desc': 'Walls placed',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(['minecraft:used'],['minecraft:.*_wall']),
    ))
