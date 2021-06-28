from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'eat_soup',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:used','minecraft:mushroom_stew']),
            mcstats.StatReader(['minecraft:used','minecraft:beetroot_soup']),
            mcstats.StatReader(['minecraft:used','minecraft:rabbit_stew']),
            mcstats.StatReader(['minecraft:used','minecraft:suspicious_stew']),
        ])
    ))
