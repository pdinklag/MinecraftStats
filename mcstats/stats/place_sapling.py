from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_sapling',
        {
            'title': 'Forester',
            'desc': 'Trees planted',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:.+_sapling'])
    ))
