from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_ender_chest',
        {
            'title': 'Grief This!',
            'desc': 'Ender chests crafted',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:crafted','minecraft:ender_chest']),
    ))
