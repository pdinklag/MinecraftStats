from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'eat_fish',
        {
            'title': 'Fish Gourmet',
            'desc': 'Fish eaten',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:used','minecraft:cooked_salmon']),
            __mcstats__.StatReader(['minecraft:used','minecraft:cooked_cod']),
            __mcstats__.StatReader(['minecraft:used','minecraft:salmon']),
            __mcstats__.StatReader(['minecraft:used','minecraft:cod']),
            __mcstats__.StatReader(['minecraft:used','minecraft:clownfish']),
            __mcstats__.StatReader(['minecraft:used','minecraft:pufferfish']),
        ])
    ))
