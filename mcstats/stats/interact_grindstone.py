from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'interact_grindstone',
        {
            'title': 'I Fix It',
            'desc': 'Grindstone interactions',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:interact_with_grindstone']),
        2219 # stat added in 1.15 Pre-Release 2
    ))
