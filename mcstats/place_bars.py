from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'place_bars',
        {
            'title': 'Jailer',
            'desc': 'Iron bars placed',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:iron_bars'])
    ))
