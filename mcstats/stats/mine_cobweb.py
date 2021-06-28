from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_cobweb',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:mined','minecraft:cobweb'])
    ))
