from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'trade',
        {
            'title': 'Trader',
            'desc': 'Villager trades',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:traded_with_villager'])
    ))
