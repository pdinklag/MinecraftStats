from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_bread',
        {
            'title': 'Baker',
            'desc': 'Breads, cakes and cookies made',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:crafted','minecraft:bread']),
            __mcstats__.StatReader(['minecraft:crafted','minecraft:cake']),
            __mcstats__.StatReader(['minecraft:crafted','minecraft:cookie']),
        ])
    ))
