from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_compass',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:compass']),
    ))
