from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'play',
        {
            'unit': 'ticks',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:custom','minecraft:play_one_minute']),
            mcstats.StatReader(['minecraft:custom','minecraft:play_time']) # 21w16a (data version 2711)
        ])
    ))
