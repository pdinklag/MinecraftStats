from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_cobweb',
        {
            'title': 'God...Damnit!',
            'desc': 'Cobweb removed',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:mined','minecraft:cobweb'])
    ))
