from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_wall',
        {
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(['minecraft:used'],['minecraft:.*_wall']),
    ))
