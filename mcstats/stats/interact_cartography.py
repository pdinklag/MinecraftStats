from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'interact_cartography',
        {
            'title': 'Cartographer',
            'desc': 'Cartography table interactions',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:interact_with_cartography_table']),
        1921 # stonecutters usable since 19w02a
    ))
