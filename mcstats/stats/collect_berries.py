from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'collect_berries',
        {
            'title': 'Berry Collector',
            'desc': 'Berries collected',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:picked_up','minecraft:glow_berries']),
            mcstats.StatReader(['minecraft:picked_up','minecraft:sweet_berries'])
        ]),
        1916 # sweet berries introduced in 18w49a
    ))
