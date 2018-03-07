from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_ground',
        {
            'title': 'Excavator',
            'desc': 'Dirt, sand and gravel mined',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:mined','minecraft:dirt']),
            mcstats.StatReader(['minecraft:mined','minecraft:gravel']),
            mcstats.StatReader(['minecraft:mined','minecraft:sand']),
        ])
    ))
