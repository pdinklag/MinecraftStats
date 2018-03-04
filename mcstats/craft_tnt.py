from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_tnt',
        {
            'title': 'Bad Intentions',
            'desc': 'TNT crafted',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:crafted','minecraft:tnt'])
    ))
