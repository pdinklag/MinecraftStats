from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_water_bucket',
        {
            'title': 'Aqueduct',
            'desc': 'Water buckets emptied',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:water_bucket'])
    ))
