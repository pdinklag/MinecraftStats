from mcstats import mcstats

mainStat = mcstats.MinecraftStat(
        'place_sign',
        {
            'title': 'README.TXT',
            'desc': 'Signs placed',
            'unit': 'int',
        },
        # subtract mined from used
        mcstats.StatSumMatchReader(['minecraft:used'],['minecraft:.+_sign']),
        1901 # signs were updated in 18w43a
    )

mcstats.registry.append(mainStat)

# Support for 1.13
mcstats.registry.append(mcstats.LegacyStat(mainStat, 1451, 1631,
    mcstats.StatReader(['minecraft:used','minecraft:sign'])
))
