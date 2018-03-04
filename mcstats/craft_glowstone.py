from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_glowstone',
        {
            'title': 'Illuminator',
            'desc': 'Glowstone crafted',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:crafted','minecraft:glowstone']),
    ))
