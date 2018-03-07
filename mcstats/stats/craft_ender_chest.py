from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_ender_chest',
        {
            'title': 'Grief This!',
            'desc': 'Ender chests crafted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:ender_chest']),
    ))
