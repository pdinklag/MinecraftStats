from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_spawner',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:mined','minecraft:spawner'])
    ))
