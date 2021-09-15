from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_cobweb',
        {
            'title': 'Silky Situation',
            'desc': 'Cobweb removed',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:mined','minecraft:cobweb'])
    ))
