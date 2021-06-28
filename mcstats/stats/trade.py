from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'trade',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:traded_with_villager'])
    ))
