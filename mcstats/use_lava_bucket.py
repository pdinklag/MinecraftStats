from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_lava_bucket',
        {
            'title': 'Napalm',
            'desc': 'Lava buckets emptied',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:lava_bucket'])
    ))
