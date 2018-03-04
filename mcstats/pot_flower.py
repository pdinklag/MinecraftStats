from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'pot_flower',
        {
            'title': 'Florist',
            'desc': 'Flowers potted',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:pot_flower'])
    ))
