from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'damage_dealt',
        {
            'title': 'Berserk!',
            'desc': 'Damage dealt',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:damage_dealt'])
    ))
