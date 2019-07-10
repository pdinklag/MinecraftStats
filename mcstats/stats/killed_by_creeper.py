from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'killed_by_creeper',
        {
            'title': 'Look Behind You',
            'desc': 'Times Killed by Creepers',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:killed_by','minecraft:creeper'])
    ))
