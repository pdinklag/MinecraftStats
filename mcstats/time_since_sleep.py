from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'time_since_sleep',
        {
            'title': 'Insomnia',
            'desc': 'Time since last sleep',
            'unit': 'ticks',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:time_since_sleep'])
    ))
