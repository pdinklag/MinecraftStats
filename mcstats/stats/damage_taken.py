from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'damage_taken',
        {
            'title': 'Ouch!',
            'desc': 'Damage taken',
            'unit': 'tenths_of_heart',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:damage_taken'])
    ))
