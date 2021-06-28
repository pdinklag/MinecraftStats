from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'interact_smoker',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:interact_with_smoker']),
        1919 # smokers usable since 18w50a
    ))
