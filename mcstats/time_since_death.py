from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'time_since_death',
        {
            'title': 'Survivor',
            'desc': 'Time since last death',
            'unit': 'ticks',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:time_since_death'])
    ))
