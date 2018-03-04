from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'eat_junkfood',
        {
            'title': 'Bottom Feeder',
            'desc': 'Junkfood items eaten',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:used','minecraft:rotten_flesh']),
            __mcstats__.StatReader(['minecraft:used','minecraft:spider_eye']),
            __mcstats__.StatReader(['minecraft:used','minecraft:poisonous_potato']),
        ])
    ))
