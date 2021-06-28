from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'damage_dealt',
        {
            'unit': 'tenths_of_heart',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:damage_dealt'])
    ))
