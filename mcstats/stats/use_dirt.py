from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_dirt',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:used','minecraft:dirt']),
            mcstats.StatReader(['minecraft:used','minecraft:rooted_dirt']),
            mcstats.StatReader(['minecraft:used','minecraft:mud'])
        ])
    ))
