from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'drop',
        {
            'title': 'Dropper',
            'desc': 'Items dropped',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:drop'])
    ))
