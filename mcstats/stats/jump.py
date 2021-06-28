from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'jump',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:jump'])
    ))
