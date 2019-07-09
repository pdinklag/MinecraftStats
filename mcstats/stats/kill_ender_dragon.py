from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_ender_dragon',
        {
            'title': 'Dragon Hunter',
            'desc': 'Ender Dragons killed',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:killed','minecraft:ender_dragon']),
    ))
