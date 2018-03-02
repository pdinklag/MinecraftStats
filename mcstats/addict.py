from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'addict',
        {
            'name': 'Addict',
            'desc': 'Time played on the server',
            'icon': 'gui/connection.png',
            'unit': 'ticks',
        },
         __mcstats__.StatReader(['minecraft:custom','minecraft:play_one_minute'])
    ))
