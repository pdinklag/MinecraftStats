from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'killed_by_creeper',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:killed_by','minecraft:creeper'])
    ))
