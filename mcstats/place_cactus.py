from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'place_cactus',
        {
            'title': 'Cactus Farmer',
            'desc': 'Cacti planted',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:cactus'])
    ))
