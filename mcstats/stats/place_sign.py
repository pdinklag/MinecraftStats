from mcstats import mcstats

mainStat = mcstats.MinecraftStat(
        'place_sign',
        {
            'title': 'README.TXT',
            'desc': 'Signs placed',
            'unit': 'int',
        },
        # subtract mined from used
        mcstats.StatDiffReader(
            mcstats.StatSumMatchReader(
                ['minecraft:used'],['minecraft:.+_sign']),
            mcstats.StatSumMatchReader(
                ['minecraft:mined'],['minecraft:.+_sign'])
        ),
        1901 # signs were updated in 18w43a
    )

mcstats.registry.append(mainStat)

# Support for 1.13
mcstats.registry.append(mcstats.LegacyStat(mainStat, 1451, 1631,
    # subtract mined from used
    mcstats.StatDiffReader(
        mcstats.StatReader(['minecraft:used','minecraft:sign']),
        mcstats.StatReader(['minecraft:mined','minecraft:sign'])
    )
))
