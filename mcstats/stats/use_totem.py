from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_totem',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:totem_of_undying'])
    ))
