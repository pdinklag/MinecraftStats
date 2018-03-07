from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_sapling',
        {
            'title': 'Forester',
            'desc': 'Trees planted',
            'unit': 'int',
        },
        # subtract mined from placed
        mcstats.StatDiffReader(
            mcstats.StatSumMatchReader(
                ['minecraft:used'],
                ['minecraft:.+_sapling']),
            mcstats.StatSumMatchReader(
                ['minecraft:mined'],
                ['minecraft:.+_sapling'])),
    ))
