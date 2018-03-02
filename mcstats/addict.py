from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftCustomStat(
        'addict',
        {
            'name': 'Addict',
            'desc': 'Time played on the server',
            'icon': 'gui/connection.png',
            'unit': 'ticks',
        },
        'minecraft:walk_one_cm'))
