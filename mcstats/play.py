from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'play',
        {
            'title': 'Addict',
            'desc': 'Time played on the server',
            'unit': 'ticks',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:play_one_minute'])
    ))
