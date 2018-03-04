from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'eat_soup',
        {
            'title': 'Soupy Caspar',
            'desc': 'Soups and stews eaten',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:used','minecraft:mushroom_stew']),
            __mcstats__.StatReader(['minecraft:used','minecraft:beetroot_soup']),
            __mcstats__.StatReader(['minecraft:used','minecraft:rabbit_stew']),
        ])
    ))
