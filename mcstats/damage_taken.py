from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'damage_taken',
        {
            'title': 'Punching Bag',
            'desc': 'Damage taken',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:damage_taken'])
    ))
