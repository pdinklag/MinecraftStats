from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'damage_shield',
        {
            'title': 'Shield',
            'desc': 'Damage blocked',
            'unit': 'tenths_of_heart',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:damage_blocked_by_shield']),
        1623 # stat added in 18w32a
    ))
