from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'play_record',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:play_record'])
    ))
