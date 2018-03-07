from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_flint',
        {
            'title': 'Pyromaniac',
            'desc': 'Fires started',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:flint_and_steel'])
    ))
