from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_ender_chest',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:ender_chest']),
    ))
