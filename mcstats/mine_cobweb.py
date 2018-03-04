from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'mine_cobweb',
        {
            'title': 'God...Damnit!',
            'desc': 'Cobweb removed',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:mined','minecraft:cobweb'])
    ))
