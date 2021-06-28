from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_fireworks',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:firework_rocket'])
    ))
