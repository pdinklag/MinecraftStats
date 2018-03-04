from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_hoe',
        {
            'title': 'Farmer',
            'desc': 'Ground blocks plowed',
            'unit': 'int',
        },
        __mcstats__.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:.+_hoe'])
    ))
