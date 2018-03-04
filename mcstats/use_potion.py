from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_potion',
        {
            'title': 'Alchemist',
            'desc': 'Potions used',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:used','minecraft:potion']),
            __mcstats__.StatReader(['minecraft:used','minecraft:splash_potion'])
        ])
    ))
