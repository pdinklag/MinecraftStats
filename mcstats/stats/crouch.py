from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'crouch',
        {
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:crouch_one_cm'])
    ))
