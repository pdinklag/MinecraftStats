from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'biomes',
        {
            'title': 'Explorer',
            'desc': 'Biomes discovered',
            'unit': 'int',
        },
        mcstats.StatListLengthReader([
            'advancements',
            'minecraft:adventure/adventuring_time',
            'criteria'
        ])
    ))
