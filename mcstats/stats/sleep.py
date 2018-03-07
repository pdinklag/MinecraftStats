from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'sleep',
        {
            'title': 'Sleepyhead',
            'desc': 'Times slept',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:sleep_in_bed'])
    ))
