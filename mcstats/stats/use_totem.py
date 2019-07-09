from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_totem',
        {
            'title': '9 lives',
            'desc': 'Totems of Undying used',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:totem_of_undying'])
    ))
