from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'sleep',
        {
            'title': 'Sleepyhead',
            'desc': 'Times slept',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:sleep_in_bed'])
    ))
