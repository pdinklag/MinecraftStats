from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'death',
        {
            'title': 'Lemming',
            'desc': 'Times died',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:deaths'])
    ))
