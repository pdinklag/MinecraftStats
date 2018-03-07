from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_compass',
        {
            'title': 'Navigator',
            'desc': 'Compasses crafted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:compass']),
    ))
