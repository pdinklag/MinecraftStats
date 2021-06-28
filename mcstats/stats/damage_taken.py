from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'damage_taken',
        {
            'unit': 'tenths_of_heart',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:damage_taken'])
    ))
