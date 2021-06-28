from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'sleep',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:sleep_in_bed'])
    ))
