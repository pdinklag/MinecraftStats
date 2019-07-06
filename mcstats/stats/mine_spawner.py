from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_spawner',
        {
            'title': 'Nope!',
            'desc': 'Spawners removed',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:mined','minecraft:spawner'])
    ))
