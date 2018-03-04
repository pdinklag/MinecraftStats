from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_sponge',
        {
            'title': 'Spongebob',
            'desc': 'Sponges dried',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:crafted','minecraft:sponge'])
    ))
