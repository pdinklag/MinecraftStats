from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'pot_flower',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:pot_flower'])
    ))
