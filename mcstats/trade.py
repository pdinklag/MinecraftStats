from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'trade',
        {
            'title': 'Trader',
            'desc': 'Villager trades',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:traded_with_villager'])
    ))
