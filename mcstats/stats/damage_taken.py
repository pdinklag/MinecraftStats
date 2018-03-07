from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'damage_taken',
        {
            'title': 'Punching Bag',
            'desc': 'Damage taken',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:damage_taken'])
    ))
