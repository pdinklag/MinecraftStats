from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'interact_anvil',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:interact_with_anvil']),
        2219 # stat added in 1.15 Pre-Release 2
    ))
