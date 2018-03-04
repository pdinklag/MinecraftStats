from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'mine_tall_grass',
        {
            'title': 'Lawnmower',
            'desc': 'Tall grass removed',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:mined','minecraft:tall_grass'])
    ))
