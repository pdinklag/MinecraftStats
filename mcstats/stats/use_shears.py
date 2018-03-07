from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_shears',
        {
            'title': 'Cutter',
            'desc': 'Shear uses',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:shears'])
    ))
