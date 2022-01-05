from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'leave_game',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:leave_game']),
        1926 # stonecutters usable since 19w04a
    ))
