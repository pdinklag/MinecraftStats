from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_paper',
        {
            'title': 'Paperboy',
            'desc': 'Paper produced',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:crafted','minecraft:paper'])
    ))
